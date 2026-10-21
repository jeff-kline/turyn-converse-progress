"""Independent exact verifier for parameterized C61 orbit-lattice certificates.

The rational LDL/enumerator and ring-tensor routines are preserved verbatim
from the separately audited 8905 checker in legacy_exact.py. This wrapper
reconstructs new prime quotients, Galois allocation orbits, norm scaling and
boxed lifts without importing the production solver or invoking PARI.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import resource
import signal
import sys
import time

from legacy_exact import (
    rref, annihilator, matmul, ldl, enumerate_short, period_tensor,
)

N = 20
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT


def factor(n):
    factors = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            factors[p] = factors.get(p,0)+1
            n //= p
        p += 1
    if n > 1:
        factors[n] = factors.get(n,0)+1
    return factors


def rotate(v, shift=1):
    return [v[(j-shift)%10] for j in range(10)] + [
        v[10+(j-shift)%10] for j in range(10)
    ]


def conjugate(v):
    return list(v[:10])+[-x for x in v[10:]]


def norm_gram(b,q):
    assert len(b)==N and all(len(row)==N for row in b)
    assert all(type(x) is int for row in b for x in row)
    cols = list(zip(*b))
    sums = [(sum(c[:10]),sum(c[10:])) for c in cols]
    out = [[0]*N for _ in range(N)]
    for j in range(N):
        for k in range(j,N):
            value = 61*sum(x*y for x,y in zip(cols[j],cols[k]))
            value -= 6*sum(x*y for x,y in zip(sums[j],sums[k]))
            assert value % q == 0, "nonintegral normalized Gram matrix"
            out[j][k] = out[k][j] = value//q
    return out


def prime_quotients(data,q):
    """Prove that all exported kernels are distinct prime ideals above q."""
    fac = factor(q)
    assert q>1 and q%4==1 and math.gcd(q,61)==1
    assert all(e==1 and p%4==1 for p,e in fac.items()), "unsupported norm domain"
    tensor = period_tensor()
    distinct = {p:set() for p in fac}
    degrees = {p:0 for p in fac}
    pairs = []
    for p,f,b0,b1 in data:
        assert p in fac and type(f) is int and 1<=f<=20
        equations = []
        for basis in (b0,b1):
            assert len(basis)==N and all(len(row)==N for row in basis)
            assert all(type(x) is int for row in basis for x in row)
            eq,piv = annihilator(basis,p)
            assert len(eq)==f
            signature = tuple(map(tuple,eq))
            assert signature not in distinct[p]
            distinct[p].add(signature)
            degrees[p] += f
            def proj(v):
                return [sum(x*y for x,y in zip(row,v))%p for row in eq]
            qt = [[proj(tensor[a][b]) for b in piv] for a in piv]
            def mul(x,y):
                return [sum(x[s]*y[t]*qt[s][t][k]
                            for s in range(f) for t in range(f))%p
                        for k in range(f)]
            columns = list(zip(*eq))
            for a in range(N):
                for b in range(N):
                    assert proj(tensor[a][b]) == mul(columns[a],columns[b])
            unit = proj([-1]*10+[0]*10)
            assert any(unit)
            def power(x,n):
                y = unit[:]
                while n:
                    if n&1:
                        y = mul(y,x)
                    x = mul(x,x)
                    n //= 2
                return y
            eye = [[int(i==j) for j in range(f)] for i in range(f)]
            frob = list(map(list,zip(*[power(v,p) for v in eye])))
            iterate = eye
            for _ in range(f):
                iterate = matmul(iterate,frob,p)
            assert iterate == eye
            delta = [[frob[i][j]-eye[i][j] for j in range(f)] for i in range(f)]
            assert len(rref(delta,p)[1]) == f-1
            equations.append(eq)
        assert rref([conjugate(row) for row in equations[0]],p)[0] == equations[1]
        pairs.append((p,equations))
    assert degrees == {p:20 for p in fac}, "prime decomposition incomplete"
    assert sum(f for p,f,b0,b1 in data)==10*len(fac)
    lookup = {
        (p,tuple(map(tuple,eq))):(j,bit)
        for j,(p,choices) in enumerate(pairs) for bit,eq in enumerate(choices)
    }
    action = []
    for j,(p,choices) in enumerate(pairs):
        images = [
            lookup[(p,tuple(map(tuple,rref([rotate(row) for row in eq],p)[0])))]
            for eq in choices
        ]
        assert images[0][0] == images[1][0] and images[0][1] != images[1][1]
        action.append(images[0])
    assert sorted(j for j,flip in action)==list(range(len(pairs)))
    return pairs,action


def allocation_orbits(action):
    """Independent exhaustive partition with witnesses sigma^r conjugation^c."""
    count = len(action)
    full = (1<<count)-1
    def step(mask):
        result = 0
        for j,(destination,flip) in enumerate(action):
            result |= (((mask>>j)&1)^flip)<<destination
        return result
    for j in range(count):
        for seed in (0,1<<j):
            v = seed
            for _ in range(10):
                v = step(v)
            assert v==seed
    seen = bytearray(1<<count)
    out = {}
    for mask in range(1<<count):
        if seen[mask]:
            continue
        members = {}
        value = mask
        for rotation in range(10):
            for c in (0,1):
                image = value ^ (full if c else 0)
                members.setdefault(image,(rotation,c))
            value = step(value)
        assert value==mask and min(members)==mask
        for image in members:
            assert not seen[image]
            seen[image] = 1
        out[mask] = members
    assert all(seen)
    return out


def burnside_count(action):
    """Count fixed masks through signed-permutation cycles, independently."""
    n=len(action)
    permutation=list(range(n))
    flips=[0]*n
    fixed=[]
    for power in range(10):
        for c in (0,1):
            seen=set()
            cycles=0
            consistent=True
            for j in range(n):
                if j in seen:
                    continue
                k=j
                parity=0
                while k not in seen:
                    seen.add(k)
                    parity ^= flips[k]^c
                    k=permutation[k]
                assert k==j
                if parity:
                    consistent=False
                cycles+=1
            fixed.append((1<<cycles) if consistent else 0)
        old=permutation
        flips=[flips[j]^action[old[j]][1] for j in range(n)]
        permutation=[action[old[j]][0] for j in range(n)]
    assert permutation==list(range(n)) and not any(flips)
    assert sum(fixed)%20==0
    return sum(fixed)//20,fixed


def check_membership(b,mask,pairs):
    for j,(p,choices) in enumerate(pairs):
        assert all(sum(row[k]*b[k][col] for k in range(N))%p==0
                   for row in choices[(mask>>j)&1] for col in range(N))


def direct_norm(v,q):
    h = {pow(2,10*j,61) for j in range(6)}
    rows = [[0]*61,[0]*61]
    for side in range(2):
        for j in range(10):
            for x in h:
                rows[side][pow(2,j,61)*x%61] = v[10*side+j]
    corr = [sum(a[j]*a[(j-k)%61] for a in rows for j in range(61))
            for k in range(61)]
    assert all(value==corr[0]-q for value in corr[1:])
    return rows


def local_invariance(q):
    """Whether the audited multiplier theorem forces the chosen H6."""
    h={pow(2,10*j,61) for j in range(6)}
    for p in factor(q):
        powers={1}
        value=p%61
        while value not in powers:
            powers.add(value)
            value=value*p%61
        if not h <= powers|{-x%61 for x in powers}:
            return False
    return True


def boxed_lifts(vectors,q):
    """All H6-invariant boxed lifts; application requires local_invariance."""
    assert q%244==121, "q does not give an odd C61 fiber"
    f=(q+1)//122
    h={pow(2,10*j,61) for j in range(6)}
    cosets=[{pow(2,j,61)*x%61 for x in h} for j in range(10)]
    totals=[(a,b) for a in range(-math.isqrt(q),math.isqrt(q)+1) if a%2==0
            for b in (-math.isqrt(q-a*a),math.isqrt(q-a*a))
            if b>0 or b<0
            if b*b+a*a==q and b%2]
    totals=sorted(set(totals))
    parity=[]
    lifts={}
    for v in sorted(vectors):
        direct_norm(v,q)
        if not all(x%2==1 for x in v[:10]) or not all(x%2==0 for x in v[10:]):
            continue
        parity.append(v)
        for x,y in totals:
            na,nb=x-6*sum(v[:10]),y-6*sum(v[10:])
            if na%61 or nb%61:
                continue
            a0,b0=na//61,nb//61
            if abs(a0)>f-1 or (a0-f+1)%4 or abs(b0)>f or b0%2!=1:
                continue
            aa,bb=[a0]*61,[b0]*61
            for j,coset in enumerate(cosets):
                for u in coset:
                    aa[u]+=v[j]
                    bb[u]+=v[10+j]
            if not all(abs(z)<=f and z%2 for z in aa[1:]+bb):
                continue
            assert sum(aa)==x and sum(bb)==y
            assert all(sum(aa[j]*aa[(j-k)%61]+bb[j]*bb[(j-k)%61] for j in range(61))
                       == (q if k==0 else 0) for k in range(61))
            lifts[tuple(aa+bb)]={"augmentation":[x,y],"A":aa,"B":bb,
                                 "period_coordinates":list(v)}
    return parity,list(lifts.values())


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--case",type=Path,required=True)
    ap.add_argument("--q",type=int,required=True)
    ap.add_argument("--streams",type=Path,nargs="+",required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--require-local-invariance",action="store_true",
                    help="Require this field census to be a Turyn necessary condition.")
    ap.add_argument("--cpu",type=int,default=1200)
    ap.add_argument("--wall",type=int,default=1500)
    args=ap.parse_args()
    args.case=args.case.resolve()
    args.streams=[p.resolve() for p in args.streams]
    args.output=args.output.resolve()
    assert 1<=args.cpu<=1200 and args.cpu<=args.wall<=1800
    resource.setrlimit(resource.RLIMIT_CPU,(args.cpu,args.cpu))
    signal.alarm(args.wall)
    start=time.process_time()
    q=args.q
    invariant=local_invariance(q)
    if args.require_local_invariance:
        assert invariant, "local symmetry does not force this field"
    prime_path=args.case/"prime_lattices.json"
    data=json.loads(prime_path.read_text())
    pairs,action=prime_quotients(data,q)
    orbits=allocation_orbits(action)
    orbit_count,fixed_mask_counts=burnside_count(action)
    assert orbit_count==len(orbits)
    print(json.dumps({"q":q,"prime_pairs":len(pairs),"total_masks":1<<len(pairs),
                      "orbits":len(orbits),"domain_cpu":time.process_time()-start}),flush=True)
    params=json.loads((args.case/"parameters.json").read_text())
    assert params["q"]==q
    assert params["canonical_representatives"]==list(orbits)
    orbit_path=args.case/"orbits.jsonl"
    seen_reps=set()
    for line in orbit_path.open():
        rep,members=json.loads(line)
        assert rep not in seen_reps and rep in orbits
        seen_reps.add(rep)
        declared={}
        for mask,r,c in members:
            assert mask not in declared and 0<=r<10 and c in (0,1)
            value=rep
            for _ in range(r):
                value=sum(((((value>>j)&1)^flip)<<dest)
                          for j,(dest,flip) in enumerate(action))
            if c:
                value^=(1<<len(pairs))-1
            assert value==mask
            declared[mask]=(r,c)
        assert set(declared)==set(orbits[rep])
    assert seen_reps==set(orbits)
    # Test the direct group mapping of an exact Gaussian norm control later.
    positives={}
    seen=set()
    nodes=0
    for path in args.streams:
        for line in path.open():
            rep,b,reported,shortrows=json.loads(line)
            assert rep in orbits and rep not in seen
            seen.add(rep)
            check_membership(b,rep,pairs)
            g=norm_gram(b,q)
            d,u,det=ldl(g)
            assert det==61**18, "proper sublattice or incorrect basis determinant"
            vectors,n=enumerate_short(d,u,10)
            nodes+=n
            columns=list(zip(*shortrows)) if shortrows else []
            signed={tuple(v) for v in columns}|{tuple(-x for x in v) for v in columns}
            assert len(vectors)==reported and set(vectors)==signed
            if vectors:
                positives[rep]={
                    tuple(sum(b[i][j]*v[j] for j in range(N)) for i in range(N))
                    for v in vectors
                }
            if len(seen)%2048==0:
                print(json.dumps({"checked_orbits":len(seen),"expected":len(orbits),
                                  "cpu":time.process_time()-start}),flush=True)
    assert seen==set(orbits), "incomplete orbit lattice stream"
    all_values=set()
    positive_masks={}
    for rep,values in positives.items():
        for mask,(r,c) in orbits[rep].items():
            transformed={tuple(conjugate(rotate(v,r)) if c else rotate(v,r))
                         for v in values}
            assert mask not in positive_masks
            positive_masks[mask]=transformed
            all_values.update(transformed)
    assert len(all_values)==sum(len(v) for v in positive_masks.values())
    gaussian={
        tuple([-a]*10+[-b]*10)
        for a in range(-math.isqrt(q),math.isqrt(q)+1)
        for b in range(-math.isqrt(q),math.isqrt(q)+1)
        if a*a+b*b==q
    }
    assert gaussian<=all_values
    parity,lifts=boxed_lifts(all_values,q)
    reference_match=None
    if q==8905:
        ref=json.loads((BASE/"pursuit-02/c61_certificate.json").read_text())
        expected={tuple(a+b) for _,_,a,b in ref["weil_generators_period_coordinates"]}
        assert all_values==expected
        assert set(parity)=={tuple(a+b) for _,_,a,b in ref["parity_generators_period_coordinates"]}
        expected_lifts={tuple(r["A"]+r["B"])
                        for r in ref["all_augmentation_positive_control_marginals"]}
        assert {tuple(r["A"]+r["B"]) for r in lifts}==expected_lifts
        assert len(positive_masks)==22 and len(all_values)==88 and len(parity)==44 and len(lifts)==8
        reference_match=True
    out={
        "status":"COMPLETE_INDEPENDENT_EXACT_CHECK","q":q,
        "local_invariance_forces_H6":invariant,
        "marginal_scope":"Complete H6-invariant boxed C61 marginals",
        "prime_pairs":len(pairs),"allocation_domain":1<<len(pairs),
        "orbit_representatives":len(orbits),"positive_orbits":len(positives),
        "positive_ideals":len(positive_masks),"weil_count":len(all_values),
        "parity_count":len(parity),"boxed_marginal_count":len(lifts),
        "gaussian_controls":len(gaussian),"reference8905_full_set_match":reference_match,
        "absolute_augmentation_spectrum":sorted({(abs(r["augmentation"][0]),abs(r["augmentation"][1]))
                                                 for r in lifts}),
        "all_values_fixed_by_rotation2":all(rotate(v,2)==list(v) for v in all_values),
        "weil_values":sorted(all_values),"parity_values":parity,"boxed_marginals":lifts,
        "prime_rotation_action":action,"exact_enumeration_nodes":nodes,
        "burnside_fixed_mask_counts":fixed_mask_counts,
        "cpu_seconds":time.process_time()-start,
        "max_rss_macos_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "interpreter":sys.executable,"isolated":True,
        "input_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in [prime_path,args.case/"parameters.json",orbit_path,*args.streams]},
        "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "legacy_exact_sha256":hashlib.sha256((HERE/"legacy_exact.py").read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k not in
                      {"weil_values","parity_values","boxed_marginals","prime_rotation_action",
                       "input_sha256"}},indent=2),flush=True)


if __name__=="__main__":
    main()
