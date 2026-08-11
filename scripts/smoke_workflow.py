import json, os, re, time
from genlayer_py import create_client, create_account
from genlayer_py.chains import testnet_bradbury

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE=os.path.abspath(os.path.join(ROOT,'..','..','..','..'))
def value(name):
    text=open(os.path.join(WORKSPACE,'accounts.env'),encoding='utf-8').read()
    return re.search(rf'^\s*{name}\s*=\s*"?([^"\r\n]+)',text,re.M).group(1).strip()
def wait(c,h): return c.wait_for_transaction_receipt(transaction_hash=h,status='ACCEPTED',retries=60,interval=30000)
def main():
    account=create_account(account_private_key=value('ACCOUNT_1_GENLAYER_PRIVATE_KEY'))
    client=create_client(chain=testnet_bradbury,account=account)
    address=json.load(open(os.path.join(ROOT,'deployment.json'),encoding='utf-8'))['contract']
    packet='AUDIT-'+str(int(time.time()))
    args=[packet,'ops-handoff-v1','PAYMENTS','Transfer custody of the deployment recovery procedure to the payments operations team.',['A stale worker may retain the prior credential.'],['Signed repository record','Public service status'], 'Revoke the alias, drain workers, verify the epoch, then reopen ingress.',['https://api.github.com/repos/SAMiiNW/relay-discipline/commits/main'],'https://www.githubstatus.com/api/v2/status.json']
    submit=client.write_contract(address=address,function_name='submit_packet',args=args); print('submitTx',submit,flush=True); wait(client,submit)
    inspect=client.write_contract(address=address,function_name='inspect_handoff',args=[packet]); print('inspectTx',inspect,flush=True); wait(client,inspect)
    print(json.dumps({'packetId':packet,'submitTx':submit,'inspectTx':inspect,'status':'ACCEPTED'},indent=2),flush=True)
if __name__=='__main__': main()
