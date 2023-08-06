from drf_spectacular.extensions import (
    OpenApiAuthenticationExtension,
    OpenApiSerializerFieldExtension,
)
from drf_spectacular.plumbing import ResolvedComponent  # NOQA
from drf_spectacular.plumbing import (
    build_basic_type,
    build_bearer_security_scheme_object,
)
from drf_spectacular.types import OpenApiTypes


class TagListSerializerFieldExtension(OpenApiSerializerFieldExtension):
    target_class = "taggit.serializers.TagListSerializerField"

    def map_serializer_field(self, auto_schema, direction):
        return build_basic_type(OpenApiTypes.STR)
