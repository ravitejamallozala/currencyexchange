import copy

from model_utils.models import TimeStampedModel

NAME_LENGTH = 60


class ExchangeBaseModel(TimeStampedModel):

    def clone(self):
        """Clones the object and returns the cloned instance
        retains the pk and clears all django populated (non-concrete fields) cache
        """
        new_obj = copy.copy(self)
        data_mapping = self.__dict__
        deep_copy_types = [list, dict]

        for each in data_mapping:
            item = data_mapping[each]
            if not each.startswith("_") and type(item) in deep_copy_types:
                setattr(new_obj, each, copy.deepcopy(item))
    class Meta:
        abstract = True
