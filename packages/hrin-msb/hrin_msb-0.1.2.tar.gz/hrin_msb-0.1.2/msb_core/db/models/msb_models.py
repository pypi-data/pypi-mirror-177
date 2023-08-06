import datetime

from django.core.serializers import serialize
from django.db import models
from django.db import models as Models
from .._constants import (COLUMN_NAME_DELETED, COLUMN_NAME_DELETED_BY, COLUMN_NAME_CREATED_AT, COLUMN_NAME_UPDATED_AT,
                          COLUMN_NAME_CREATED_BY, COLUMN_NAME_UPDATED_BY, COLUMN_NAME_ACTIVE, COLUMN_NAME_DELETED_AT)
from msb_core.wrappers.encryption import Cipher


class MsbModelManager(models.Manager):
	_default_filters = {}

	def _get_filtered_queryset(self, **filters):
		_query_set = super(MsbModelManager, self).get_queryset()
		query_filters = {}
		for filtername, filtervalue in filters.items():
			if hasattr(self.model, filtername):
				query_filters[filtername] = filtervalue
		return _query_set.filter(**query_filters)

	def get(self, *args, **kwargs):
		filters = {**kwargs}
		pk = kwargs.get('pk')
		if pk is not None and isinstance(pk, str):
			filters['pk'] = int(Cipher.decrypt(pk))
		return super(MsbModelManager, self).get(*args, **filters)

	@property
	def deleted(self):
		return self._get_filtered_queryset(**{COLUMN_NAME_DELETED: True})

	def get_queryset(self):
		return self._get_filtered_queryset(**{COLUMN_NAME_DELETED: False, **self._default_filters})


class MsbModel(Models.Model):
	_private_fields = []
	_identifier_fields = 'id'

	class Meta:
		abstract = True

	@property
	def related_fields(self):
		fields = []
		for field in self._meta.fields:
			if field.get_internal_type() in ['ForeignKey']:
				fields.append(field.name)
		return fields

	def dict(self, encrypted=True):
		try:
			return {
				k: v if (k not in [
					self._meta.pk.attname, *self._private_fields
				] or not encrypted) else Cipher.encrypt(v)
				for k, v in super().__dict__.items()
				if not k.startswith('__') and not k.startswith('_') and not callable(k)
			}

		except Exception:
			return dict()

	@property
	def serialized(self):
		return serialize('python', [self])

	def current_timestamp(self):
		return datetime.datetime.now()

	def delete(self, deleted_by=None, using=None, keep_parents=False):
		if hasattr(self, COLUMN_NAME_DELETED):
			self.__setattr__(COLUMN_NAME_DELETED, True)

		if hasattr(self, COLUMN_NAME_DELETED_BY):
			self.__setattr__(COLUMN_NAME_DELETED_BY, deleted_by)

		self.save()
		return True

	def __str__(self):
		return f"< {self.__class__.__name__}, pk[{self.pk}]  >"

	def __unicode__(self):
		return self.__str__()


class MsbMetaModel(MsbModel):
	class Meta:
		abstract = True

	updated_at = models.DateTimeField(db_column=COLUMN_NAME_UPDATED_AT, auto_now=True)
	updated_by = models.IntegerField(db_column=COLUMN_NAME_UPDATED_BY, null=True, default=None)
	created_at = models.DateTimeField(db_column=COLUMN_NAME_CREATED_AT, auto_now_add=True)
	created_by = models.IntegerField(db_column=COLUMN_NAME_CREATED_BY, null=True, default=None)
	is_deleted = models.BooleanField(db_column=COLUMN_NAME_DELETED, default=False, null=False)
