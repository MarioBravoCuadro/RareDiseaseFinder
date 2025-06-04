from src.rarediseasefinder.orchestrator.IWorkflow import IWorkflow


class Orchestrator:

    server = None
    workflows = []


    def __init__(self):
        pass
    def start_workflow(self,workflow):
        pass

    def get_if_all_steps_available(self, workflow:IWorkflow):
        pass

    def get_avaliable_steps(self, workflow:IWorkflow):
        pass

    def decode_search_params(self,searchConfigFilter):
        pass

    def get_workflows(self):
        #Devuelve un json con los workflows disponibles para mostrar en el front
        pass

    def get_workflow(self,seleccion):
        #devuelve el workflow de la lista de workflows
        pass

    def set_workflow_search_term(self, search_term):
        #añade en el workflow el termino de busqueda introducido en la barra de busqueda
        pass

    def get_workflow_instruction_json(self, workflow:IWorkflow):
        #devuelve el json con el árbol creado en el workflow
        pass

    def get_minium_methods_from_workflow(self, workflow:IWorkflow):
        #devuelve una lista con los métodos mínimos de todas las funciones de un workflow
        pass
    
    def get_optional_methods_from_workflow(self, workflow:IWorkflow):
        #devuelve una lista con los métodos mínimos de todas las funciones de un workflow
        pass


    def update_selected_optional_methods(self, list_of_methods):
        #devuelve una lista con los métodos opcionales devueltos
        pass
