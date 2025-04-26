---
config:
  theme: dark
  look: classic
  layout: elk
---
classDiagram
direction TB
    class IWorkflowStep {
	    +getStatus()
	    +process()
	    +revert()
    }
    class WorkflowStep {
	    +getStatus()
	    +process()
	    +revert()
    }
    class Orchestrator {
	    +availableSteps[]
	    +createWorkflow(workflowSteps[])
	    +startWorkflow(workflow)
	    +getAvailableSteps()
	    +decodeSearchParams(searchConfigFilters)
    }
    class Cliente {
    }
    class Parser {
    }

    class IWorkflow {
        +getSteps()
        +getAvailableSteps()
    }

    class Workflow {
	    +getSteps()
	    +getAvailableSteps()
    }
    class Processor {
	    +getData()
	    +getData2()
    }

    WorkflowStep ..|> IWorkflowStep
    Orchestrator o-- IWorkflow : tiene
    Workflow ..|> IWorkflow
    WorkflowStep --> Processor : uses
    Processor --> Cliente : uses
    Processor --> Parser : uses
    Workflow *-- IWorkflowStep
