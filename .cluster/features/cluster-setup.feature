Feature: Preparing the sweep host

  The series runs on a machine this repository does not own, so the host is asked what it has
  before it is told what it must look like — and it is left alone while a sweep is in progress.
  Everything below is the contract the workflow branches on: the facts a probe reports, the exit
  codes a check returns, and the one refusal that has no override.

  Scenario: A host with no GPU is offered the development engine
    Given a host with no NVIDIA driver
    When the provisioner probes it
    Then it reports cpu_only=1
    And it offers the ollama engine

  Scenario: A host with a GPU big enough for the series is offered vLLM and shards
    Given a host with 24576 MiB of VRAM
    When the provisioner probes it
    Then it offers the vllm engine
    And it offers 2 workers

  Scenario: Sharding is capped however large the GPU is
    Given a host with 98304 MiB of VRAM
    When the provisioner probes it
    Then it offers 4 workers

  Scenario: A host that has never been provisioned says so
    Given a host that has never been provisioned
    When the provisioner checks it
    Then it exits with 10
    And it says nothing provisioned

  Scenario: A host that drifted from the configuration says so
    Given a host provisioned with pixi 0.0.1
    When the provisioner checks it
    Then it exits with 11
    And it says the host drifted

  Scenario: A host is not reconfigured while a sweep is running
    Given a host provisioned for the current configuration
    And a sweep is in progress on it
    When the provisioner checks it
    Then it exits with 12
    And it says a sweep is running

  Scenario: A host with no GPU refuses to serve a measurement
    Given a host with no NVIDIA driver
    When the provisioner is asked to provision it
    Then it exits with 13
    And it names --allow-cpu as the way past it

  Scenario: The plan names the frozen install it would run
    Given a host with 24576 MiB of VRAM
    When the provisioner plans for it
    Then the plan includes "pixi install --frozen -e experiment"
