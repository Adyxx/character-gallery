from .reference_registry import REFERENCEABLE_MODELS


def resolve_reference(reference_type, slug):
    model = REFERENCEABLE_MODELS.get(reference_type.lower())

    if model is None:
        return None

    return model.objects.filter(slug=slug).first()