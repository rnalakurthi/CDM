from typing import Union, Optional

from cdm.enums import CdmObjectType
from cdm.objectmodel import CdmCorpusContext, CdmEntityReference

from . import utils
from .cdm_object_ref_persistence import CdmObjectRefPersistence
from .constant_entity_persistence import ConstantEntityPersistence
from .types import EntityReference


class EntityReferencePersistence(CdmObjectRefPersistence):
    @staticmethod
    def from_data(ctx: CdmCorpusContext, data: Union[str, EntityReference]) -> Optional[CdmEntityReference]:
        if not data:
            return None
        from .entity_persistence import EntityPersistence

        simple_reference = True
        entity = None
        applied_traits = None

        if isinstance(data, str):
            entity = data
        else:
            simple_reference = False
            if isinstance(data.entityReference, str):
                entity = data.entityReference
            elif data.entityReference.get('entityShape'):
                entity = ConstantEntityPersistence.from_data(ctx, data.entityReference)
            else:
                entity = EntityPersistence.from_data(ctx, data.entityReference)

        entity_reference = ctx.corpus.make_ref(CdmObjectType.ENTITY_REF, entity, simple_reference)

        if not isinstance(data, str) and entity_reference:
            applied_traits = utils.create_trait_reference_array(ctx, data.get('appliedTraits'))
            entity_reference.applied_traits.extend(applied_traits)

        return entity_reference
