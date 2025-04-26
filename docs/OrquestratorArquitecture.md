# Diagrama de clases del orquestador

```mermaid
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
WorkflowStep ..|> IWorkflowStep

class Orchestrator {
    +availableSteps[]
    +createWorkflow(workflowSteps[])
    +startWorkflow(workflow)
    +getAvailableSteps()
    +decodeSearchParams(searchConfigFilters)
}

class Processor {
    +getData()
}

class Cliente

class Parser

class Workflow {
    +getSteps()
    +getAvailableSteps()
}

Orchestrator --> Workflow : tiene
WorkflowStep --> Processor : uses
WorkflowStep --* Workflow : formado por
Processor --> Cliente : uses
Processor --> Parser : uses
