from conftest import CONTRACT
import pytest
def submit_valid(c,direct_vm,packet_id,protocol_id='ops-v1',recipient='PAYMENTS'):
    direct_vm.mock_web(r'evidence\.example',{'status':200,'body':'rotation window=RW-42 status=ready dependencies=worker-pool recovery=rollback signed=ops-key'})
    direct_vm.mock_web(r'attestation\.example',{'status':200,'body':'recipient=PAYMENTS accepted=true scope=RW-42 timestamp=2026-08-11T12:00Z signature=payments-key'})
    direct_vm.mock_llm(r'Summarize independently checkable.*','Signed operational record RW-42 is ready, depends on worker-pool, and has a rollback procedure.')
    direct_vm.mock_llm(r'Extract the recipient identity.*','PAYMENTS accepted custody for RW-42 at 2026-08-11T12:00Z, signed by payments-key.')
    c.submit_packet(packet_id,protocol_id,recipient,'Transfer responsibility for the active rotation window.',['replay lag'],['worker pool'],'revert alias and drain workers',['https://evidence.example/record.json'],'https://attestation.example/acceptance.json')
def test_packet_lifecycle(direct_vm,direct_deploy,direct_alice):
    c=direct_deploy(CONTRACT);direct_vm.sender=direct_alice
    c.create_protocol('ops-v1','Operations handoff','PAYMENTS',['objective','risk','recovery'],['hidden dependency'],'1.0')
    submit_valid(c,direct_vm,'PKT-1')
    direct_vm.mock_llm(r'.*RelayDiscipline.*','{"gate":"READY_WITH_ACK","risk":"MEDIUM","missing_obligations":[],"recommended_recipient_class":"PAYMENTS","confidence":88,"reason":"Complete with acknowledgement."}')
    c.inspect_handoff('PKT-1');assert c.get_decision('PKT-1')['gate']=='READY_WITH_ACK'
    assert c.get_packets_page(0,10)['total']==1
    assert c.get_decision('PKT-1')['proof'].startswith('0x5244')
    with pytest.raises(Exception):c.inspect_handoff('PKT-1')

def test_missing_obligation_cannot_settle_ready(direct_vm,direct_deploy,direct_alice):
    c=direct_deploy(CONTRACT);direct_vm.sender=direct_alice
    c.create_protocol('ops','Operations','PAYMENTS',['objective','risk','recovery'],[],'1.0')
    submit_valid(c,direct_vm,'PKT-M','ops')
    direct_vm.mock_llm(r'.*RelayDiscipline.*','{"gate":"READY","risk":"LOW","missing_obligations":["risk disclosure"],"recommended_recipient_class":"PAYMENTS","confidence":90,"reason":"Missing risk."}')
    c.inspect_handoff('PKT-M');assert c.get_decision('PKT-M')['gate']=='INCOMPLETE'

def test_wrong_recipient_forces_reroute(direct_vm,direct_deploy,direct_alice):
    c=direct_deploy(CONTRACT);direct_vm.sender=direct_alice
    c.create_protocol('ops','Operations','PAYMENTS',['objective'],[],'1.0')
    submit_valid(c,direct_vm,'PKT-R','ops','UNKNOWN')
    direct_vm.mock_llm(r'.*RelayDiscipline.*','{"gate":"READY","risk":"LOW","missing_obligations":[],"recommended_recipient_class":"SECURITY","confidence":90,"reason":"Wrong route."}')
    c.inspect_handoff('PKT-R');assert c.get_decision('PKT-R')['gate']=='REROUTE'
