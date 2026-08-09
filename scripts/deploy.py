import json,os,re
from genlayer_py import create_client,create_account
from genlayer_py.chains import testnet_bradbury
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));WORKSPACE=os.path.abspath(os.path.join(ROOT,'..','..','..','..'))
def value(name):
    text=open(os.path.join(WORKSPACE,'accounts.env'),encoding='utf-8').read();m=re.search(rf'^\s*{name}\s*=\s*"?([^"\r\n]+)',text,re.M)
    if not m:raise SystemExit(name+' missing')
    return m.group(1).strip()
def find(x):
    if isinstance(x,dict):
        if x.get('recipient') and str(x.get('tx_execution_result',''))=='1':return x['recipient']
        for k,v in x.items():
            if k in ('contract_address','contractAddress') and isinstance(v,str):return v
            r=find(v)
            if r:return r
    if isinstance(x,list):
        for v in x:
            r=find(v)
            if r:return r
def main():
    key=value('ACCOUNT_1_GENLAYER_PRIVATE_KEY');username=value('ACCOUNT_1_GITHUB_USERNAME')
    if username!='SAMiiNW':raise SystemExit('Account slot mismatch')
    account=create_account(account_private_key=key);print('Deployer',account.address,flush=True)
    c=create_client(chain=testnet_bradbury,account=account);code=open(os.path.join(ROOT,'contracts','contract.py'),encoding='utf-8').read()
    h=c.deploy_contract(code=code,args=[]);print('deployTx',h,flush=True);receipt=c.wait_for_transaction_receipt(transaction_hash=h,status='ACCEPTED',retries=60,interval=30000);address=find(receipt)
    if not address:raise SystemExit('No contract address in accepted receipt')
    seed_args=['ops-handoff-v1','Operational custody handoff','PAYMENTS',['clear objective','known risks','recovery path','bounded dependencies'],['hidden dependency','missing rollback'],'2.0']
    seed=c.write_contract(address=address,function_name='create_protocol',args=seed_args);print('seedTx',seed,flush=True);c.wait_for_transaction_receipt(transaction_hash=seed,status='ACCEPTED',retries=60,interval=30000)
    out={'contract':address,'deployTx':h,'seedTx':seed,'network':'testnet-bradbury','version':'2.0','deployer':account.address};open(os.path.join(ROOT,'deployment.json'),'w',encoding='utf-8').write(json.dumps(out,indent=2));print(json.dumps(out),flush=True)
if __name__=='__main__':main()
