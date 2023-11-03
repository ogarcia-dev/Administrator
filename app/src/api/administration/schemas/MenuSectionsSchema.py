from pydantic import (
    BaseModel,
    validator
)



class MenuSectionsRequestSchema(BaseModel):
    sidebar_menu_group: str
    sidebar_menu_separator: bool = False
    sidebar_menu_selected: bool = False
    sidebar_menu_active: bool = False
    sidebar_menu_system: str

    @validator("sidebar_menu_group")
    def sidebar_menu_group_validator(cls, sidebar_menu_group: str):
        if len(sidebar_menu_group) < 1 or len(sidebar_menu_group) > 255:
            raise ValueError("La longitud del Nombre del rol debe tener entre 1 y 255 caracteres.")
        return sidebar_menu_group.strip().replace(" ", "_")
    
    @validator("sidebar_menu_system")
    def sidebar_menu_system_validator(cls, sidebar_menu_system: str):
        if sidebar_menu_system is None:
            raise ValueError("El campo del sistema del menú de la barra lateral es obligatorio")
        return sidebar_menu_system



class MenuSectionsItemsRequestSchema(BaseModel):
    sidebar_item_icon: str
    sidebar_item_label: str
    sidebar_item_route: str
    sidebar_item_expanded: bool = False
    sidebar_item_active: bool = False
    sidebar_item_menu: str
    sidebar_item_children: str

    @validator("sidebar_item_icon")
    def sidebar_item_icon_validator(cls, sidebar_item_icon: str):
        if len(sidebar_item_icon) < 1 or len(sidebar_item_icon) > 255:
            raise ValueError("La longitud del nombre del icono del elemento de la barra lateral debe tener entre 1 y 255 caracteres.")
        return sidebar_item_icon.strip()
    
    @validator("sidebar_item_route")
    def parameter_value1_validator(cls, sidebar_item_route: str):
        if len(sidebar_item_route) < 1 or len(sidebar_item_route) > 512:
            raise ValueError("La longitud de la ruta del elemento de la barra lateral debe tener entre 1 y 512 caracteres.")
        return sidebar_item_route.strip()
    
    @validator("sidebar_item_menu")
    def sidebar_item_menu_validator(cls, sidebar_item_menu: str):
        if sidebar_item_menu is None:
            raise ValueError("El campo del elemento del menú de la barra lateral es obligatorio.")
        return sidebar_item_menu
    
    @validator("sidebar_item_children")
    def sidebar_item_children_validator(cls, sidebar_item_children: str):
        if sidebar_item_children is None:
            raise ValueError("El campo secundario del menú de la barra lateral es obligatorio.")
        return sidebar_item_children