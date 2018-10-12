require '/tmp/kitchen/tests/samodelkin/spec/helper_spec.rb'

describe package( 'python-requests' ) do
    it { should be_installed }
    end

describe file( '/usr/local/sbin/samodelkin.py' ) do
    it { should exist }
    end

describe file( '/etc/samodelkin/samodelkin.yaml' ) do
    it { should exist }
    end

describe file( '/etc/systemd/system/samodelkin.service' ) do
    it { should exist }
    end

describe service('samodelkin') do
  it { should be_running.under('systemd') }
  end
