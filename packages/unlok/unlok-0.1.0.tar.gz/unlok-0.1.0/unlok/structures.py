""" Strucutre Registration

"""


from unlok.api.schema import ScopeFragment, Search_scopesQuery, aaget_scope


try:
    from arkitekt.structures.default import get_default_structure_registry
    from arkitekt.widgets import SearchWidget

    structure_reg = get_default_structure_registry()
    structure_reg.register_as_structure(
        ScopeFragment,
        identifier="@lok/scope",
        expand=aaget_scope,
        shrink=lambda x: x.key,
        default_widget=SearchWidget(query=Search_scopesQuery.Meta.document),
    )

except ImportError:
    structure_reg = None
