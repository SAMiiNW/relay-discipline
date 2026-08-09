from conftest import CONTRACT
import pytest
def test_packet_lifecycle(direct_vm,direct_deploy,direct_alice):
    c=direct_deploy(CONTRACT);direct_vm.sender=direct_alice
    c.create_protocol('ops-v1','Operations handoff','PAYMENTS',['objective','risk','recovery'],['hidden dependency'],'1.0')
    c.submit_packet('PKT-1','ops-v1','PAYMENTS','Transfer responsibility for the active rotation window.',['replay lag'],['worker pool'],'revert alias and drain workers',['runbook attached'])
    direct_vm.mock_llm(r'.*RelayDiscipline.*','{"gate":"READY_WITH_ACK","risk":"MEDIUM","missing_obligations":[],"recommended_recipient_class":"PAYMENTS","confidence":88,"reason":"Complete with acknowledgement."}')
    c.inspect_handoff('PKT-1');assert c.get_decision('PKT-1')['gate']=='READY_WITH_ACK'
    assert c.get_packets_page(0,10)['total']==1
    assert c.get_decision('PKT-1')['proof'].startswith('0x5244')
    with pytest.raises(Exception):c.inspect_handoff('PKT-1')

def test_missing_obligation_cannot_settle_ready(direct_vm,direct_deploy,direct_alice):
    c=direct_deploy(CONTRACT);direct_vm.sender=direct_alice
    c.create_protocol('ops','Operations','PAYMENTS',['objective','risk','recovery'],[],'1.0')
    c.submit_packet('PKT-M','ops','PAYMENTS','Transfer the active operational responsibility safely.',[],[],'rollback available',[])
    direct_vm.mock_llm(r'.*RelayDiscipline.*','{"gate":"READY","risk":"LOW","missing_obligations":["risk disclosure"],"recommended_recipient_class":"PAYMENTS","confidence":90,"reason":"Missing risk."}')
    c.inspect_handoff('PKT-M');assert c.get_decision('PKT-M')['gate']=='INCOMPLETE'

def test_wrong_recipient_forces_reroute(direct_vm,direct_deploy,direct_alice):
    c=direct_deploy(CONTRACT);direct_vm.sender=direct_alice
    c.create_protocol('ops','Operations','PAYMENTS',['objective'],[],'1.0')
    c.submit_packet('PKT-R','ops','UNKNOWN','Transfer the active operational responsibility safely.',[],[],'rollback available',[])
    direct_vm.mock_llm(r'.*RelayDiscipline.*','{"gate":"READY","risk":"LOW","missing_obligations":[],"recommended_recipient_class":"SECURITY","confidence":90,"reason":"Wrong route."}')
    c.inspect_handoff('PKT-R');assert c.get_decision('PKT-R')['gate']=='REROUTE'
