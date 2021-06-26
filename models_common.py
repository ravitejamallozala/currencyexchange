import copy

from model_utils.models import TimeStampedModel
from django.utils.functional import cached_property
import django.db.models.options as options

NAME_LENGTH = 60

options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    "fetch_old_instance",
)


class ExchangeBaseModel(TimeStampedModel):
    @cached_property
    def old_instance(self):
        if hasattr(self, "cur_saved_instance") and  self.cur_saved_instance:
            return self.cur_saved_instance
        else:
            cur_saved_instance = (
                self.__class__.objects.filter(pk=self.id).first() if self.id else None
            )
            self.cur_saved_instance = cur_saved_instance
            return cur_saved_instance

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

    def save(self, *args, **kwargs):
        self.full_clean()
        if getattr(self._meta, "fetch_old_instance", False):
            self.old_instance
        super(ExchangeBaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
