"""Continue candidate repair/full verification/replay without accepting partial proof.
Runs sequential stages, each full verification uses at most three CPU workers.
Stops visibly on budget exhaustion or any validation error; never publishes.
"""
import argparse,json,os,subprocess,sys,time,traceback
from pathlib import Path
from fractions import Fraction as F
from mixed_net_audit import candidate_net
ROOT=Path(__file__).resolve().parents[2]
CODE=Path(__file__).resolve().parent


def pipeline(base,round_index,source,workers,wait_current=False,reprice_above=None,reprice_target=F('20.97'),reprice_rounds=3):
    base=base.resolve();source=source.resolve()
    candidate_meta=json.loads((source/'mixed-candidate.json').read_text())
    budget=F(candidate_meta['n'])-F(1,1000);count=candidate_net(candidate_meta)[1]+1
    if reprice_above is not None and candidate_meta['n']!=21:raise ValueError('Adaptive support pricing currently supports n21 only')
    label=f'n{candidate_meta["n"]} L{float(F(candidate_meta["L"])):g}'
    state={'status':'RUNNING','round':round_index,'source':str(source),'workers':workers,'pid':os.getpid(),'L':candidate_meta['L'],'budget':str(budget)}
    def save(**kwargs):
        state.update(kwargs);state['updated_epoch']=time.time()
        tmp=base/'pipeline-status.tmp';tmp.write_text(json.dumps(state,indent=2)+'\n');tmp.replace(base/'pipeline-status.json')
        print(json.dumps(state),flush=True)
    def watch(message):
        p=ROOT/'docs/stock/watch.md';s=p.read_text();marker='**Codex混合4.985・母艦研究：**' if F(candidate_meta['L'])==F('4.985') else f'**Codex混合n{candidate_meta["n"]}・母艦研究：**'
        if marker not in s:return
        a=s.index(marker);b=s.index('\n\n',a)
        record='2026-09-26-162-mixed-ladder-4985' if F(candidate_meta['L'])==F('4.985') else ('2026-09-27-20-mixed-n12-proof' if candidate_meta['n']==12 else '2026-09-27-19-mixed-variable-net')
        s=s[:a]+marker+' '+message+f' `{base.relative_to(ROOT)}/pipeline-status.json` に工程状態を保存。検証最大{workers}プロセス。既存本番への変更なし。[研究記録](../flow/2026-09/{record}.md)。'+s[b:]
        p.write_text(s)
    def run(script,args,log):
        env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONPATH=str(CODE))
        with log.open('w') as f:
            subprocess.run([sys.executable,str(CODE/script),*map(str,args)],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    save(stage='starting')
    try:
        if wait_current:
            save(stage='waiting_for_existing_scan')
            deadline=time.monotonic()+14400
            while True:
                try:
                    current=json.loads((base/f'round{round_index}'/'summary.json').read_text())
                    if current['complete_angles']==count:break
                except (FileNotFoundError,json.JSONDecodeError):
                    pass
                if time.monotonic()>deadline:raise RuntimeError('Existing scan did not finish within four hours')
                time.sleep(5)
        if not (base/f'round{round_index}'/'summary.json').exists():
            save(stage='full_verification',verified_angles=0)
            watch(f'{label}混合候補の初回全{count}角度検証を開始。')
            run('mixed_full_verify.py',['--candidate',source/'mixed-candidate.json','--out',base/f'round{round_index}','--workers',workers,'--budget',budget],base/f'round{round_index}.log')
        while True:
            scan=base/f'round{round_index}'
            summary=json.loads((scan/'summary.json').read_text())
            partial_failure=summary['status'] in ('STOPPED_AFTER_EXACT_DEFICIT','PRIORITY_DEFICITS_REQUIRE_REPAIR','DEFICITS_REQUIRE_REPAIR')
            assert summary['complete_angles']==count or partial_failure,'Incomplete scan without an exact failure is not repair input'
            if partial_failure:assert any(r['status'] in ('ANGLE_BELOW_GAMMA','AXIS_BELOW_GAMMA') for r in summary['records'].values())
            if summary['verified_angles']==count:
                save(stage='full_replay',round=round_index,verified_angles=count)
                watch(f'{label}混合候補 round{round_index} は{count}/{count}通過。全角度の再実行検証中。')
                run('verify_mixed_full_proof.py',[scan,'--workers',workers],base/f'replay{round_index}.log')
                result=json.loads((scan/'certificate.json').read_text());assert result['status']=='ALL_ANGLES_VERIFIED_AND_REPLAYED'
                save(status='COMPLETE',stage='certificate',certificate=str(scan/'certificate.json'))
                watch(f'{label}混合候補 round{round_index} は{count}/{count}通過・全角度再実行済み。証明書は `{scan.relative_to(ROOT)}/certificate.json`。公開・本番採用は未実施。')
                return
            target=base/f'repair{round_index+1}'
            save(stage='repair',round=round_index,verified_angles=summary['verified_angles'])
            watch(f'{label}混合候補 round{round_index} は{summary["verified_angles"]}/{count}通過。厳密反例・広域探索を追加して repair{round_index+1} を実行中。')
            run('mixed_full_repair.py',['--source',source,'--scan',scan,'--out',target],base/f'repair{round_index+1}.log')
            repaired=json.loads((target/'results.json').read_text())
            mass=F(repaired['mass']);save(mass=str(mass))
            if reprice_above is not None and mass>reprice_above:
                priced=base/f'pricing{round_index+1}'
                save(stage='support_pricing',source=str(target))
                watch(f'{label}混合候補の修復質量{float(mass):.10f}。全配置・支持を保持し、支持追加で予算余裕を回復中。')
                run('mixed_ladder_price.py',['--source',target,'--out',priced,'--rounds',reprice_rounds,'--target-mass',reprice_target],base/f'pricing{round_index+1}.log')
                pricing_state=json.loads((priced/'status.json').read_text());target=Path(pricing_state['latest'])
                mass=F(pricing_state['mass']);save(mass=str(mass),source=str(target))
                if mass<=budget:
                    assert (target/'mixed-candidate.json').exists() and (target/'exact-rechecks.json').exists(),'Pricing candidate lacks rational replay'
            if mass>budget:
                save(status='NEEDS_RESEARCH',stage='budget_exhausted')
                watch(f'{label}混合候補の自動反復は予算超過で停止。質量{float(mass):.10f}。部分通過を証明とは扱わない。')
                return
            source=target;round_index+=1;scan=base/f'round{round_index}'
            save(stage='full_verification',round=round_index,source=str(source),verified_angles=0)
            watch(f'{label}混合候補 round{round_index} の全{count}角度を検証中。修復後質量{float(mass):.10f}を{float(budget):g}へ有理拡大。')
            run('mixed_full_verify.py',['--candidate',target/'mixed-candidate.json','--out',scan,'--workers',workers,'--budget',budget],base/f'round{round_index}.log')
    except BaseException as exc:
        save(status='NEEDS_RESEARCH',stage='error',error=repr(exc),traceback=traceback.format_exc())
        watch(f'{label}混合候補の自動反復は検査エラーで停止。round{round_index}、詳細は pipeline-status.json。未証明。')
        raise

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--round',type=int,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--workers',type=int,default=3);p.add_argument('--wait-current',action='store_true');p.add_argument('--reprice-above',type=F);p.add_argument('--reprice-target',type=F,default=F('20.97'));p.add_argument('--reprice-rounds',type=int,default=3);a=p.parse_args();assert 1<=a.workers<=3
    if a.reprice_above is not None:assert 0<a.reprice_target<a.reprice_above<=F('20.999') and a.reprice_rounds>0
    pipeline(a.base,a.round,a.source,a.workers,a.wait_current,a.reprice_above,a.reprice_target,a.reprice_rounds)
