from taggit.managers import TaggableManager

from django.utils.translation import ugettext_lazy as _

from django.db import models

class City(models.Model):
	name = models.CharField(max_length=64, verbose_name=_('name'))
	slug = models.SlugField()
	
	class Meta:
		verbose_name=_('city')
		verbose_name_plural=_('cities')

	def __unicode__(self):
		return self.name

class Country(models.Model):
	name = models.CharField(max_length=64, verbose_name=_('name'))
	slug = models.SlugField()

	class Meta:
		verbose_name=_('country')
		verbose_name_plural=_('countries')

	def __unicode__(self):
		return self.name

class Sector(models.Model):
	name = models.CharField(max_length=64, verbose_name=_('name'))
	slug = models.SlugField()

	class Meta:
		verbose_name=_('sector')
		verbose_name_plural=_('sectors')

	def __unicode__(self):
		return self.name
	
class ConsumerRelation(models.Model):
	role = models.CharField(max_length=20)

	class Meta:
		verbose_name=_('consumer relation')
		verbose_name_plural=_('consumer relations')

	def __unicode__(self):
		return self.role

class Brand(models.Model):
	owner = models.ForeignKey('Organisation')
	name = models.CharField(max_length=20)
	slug = models.SlugField()

	class Meta:
		verbose_name=_('brand')
		verbose_name_plural=_('brands')

	def __unicode__(self):
		return self.name

class Identifier(models.Model):
	""" Identifier which company require to identify a user in the letter """
	name = models.CharField(max_length=20)
	organisation = models.ForeignKey('Organisation')

	class Meta:
		verbose_name=_('consumer identifier')
		verbose_name_plural=_('consumer identifiers')

class CollectedInformation(models.Model):
	""" Information which companies have about an user"""
	
	name = models.CharField(max_length=200, blank=True, help_text="")

	class Meta:
		verbose_name=_('collected information')
		verbose_name_plural=_('collected information')

	def __unicode__(self):
		return self.name

class Organisation(models.Model):
	""" A model representing an organisation. """

	name = models.CharField(max_length=200, verbose_name=_('name'), help_text="De officiele naam van de organisatie")
	""" Official name of organisation. """
	short_name = models.CharField(max_length=200, blank=True, verbose_name=('short name'), help_text=('A short name for an organisation.'))
	kvknumber = models.CharField(max_length=200, blank=True)
	street_address = models.CharField(max_length=200, verbose_name=_('street address'), blank=True)
	housenr = models.CharField(max_length=20, verbose_name=_('house number'), blank=True)
	answernr = models.CharField(max_length=20, verbose_name=_('answer number'), blank=True)
	postbus = models.CharField(max_length=20, blank=True)
	postcode = models.CharField(max_length=20, blank=True)
	city = models.ForeignKey(City, blank=True, null=True)
	country = models.ForeignKey(Country, blank=True, null=True)
	sector = models.ForeignKey(Sector, blank=True, null=True)
	website = models.CharField(max_length=200, blank=True)
	tags = TaggableManager()
	consumerrelation = models.ManyToManyField(ConsumerRelation, blank=True, null=True,
	     verbose_name='consumer relation',
	     help_text=_('The sort of relations this organisation has with consumers.'))
	collectedinformation = models.ManyToManyField(CollectedInformation, blank=True, null=True,
	     verbose_name=('collected information'),
	     help_text=_('The sort of information this organisation gathers about consumers.'))
	relation = models.ManyToManyField("self", through="Relation",
		symmetrical=False, blank=True, null=True)

	class Meta:
		verbose_name=_('organisation')
		verbose_name_plural=_('organisations')

	def __unicode__(self):
		return self.name

class RelationType(models.Model):
	""" Types of relationships. """

	name = models.CharField(max_length=64, verbose_name=_('name'))
	slug = models.SlugField()

	class Meta:
		verbose_name = _('relation type')
		verbose_name_plural = _('relation types')

	def __unicode__(self):
		return self.name

class Relation(models.Model):
	""" A relation between two companies """
	
	from_organisation = models.ForeignKey(Organisation, 
	                                      related_name='from',
	                                      verbose_name=_('from'))
	to_organisation = models.ForeignKey(Organisation, 
	                                    related_name='to',
	                                    verbose_name=_('to'))
	type = models.ForeignKey(RelationType)

class CPBRegistration(models.Model):
	""" A database registered with the CPB. This
		model should match the data in the public 
		BKR register as closely as possible. 

		TODO: Either directly contact the CPB about
		their datastructure and/or regular data
		synchronization of the public register or
		make a real good study of register access results.
		
		This model should be intelligent and do stuff like:
		1) We fill in the registration number.
		2) Go out to CPB and request all available information
		   about stored data, intended use etcetera.
		3) Fill this into our own database.
		4) Update the organisation with the kinds of data
		   stored by this party.
	    
		Reference: http://www.cbpweb.nl/Pages/ind_reg_meldreg.aspx
	"""
	
	organisation = models.ForeignKey(Organisation)	  
	# To do: add a validator here making sure that the result is always 7 digits long.
	registration_number = models.PositiveIntegerField(primary_key=True, verbose_name=_('registration number'))
	name = models.CharField(max_length=255, verbose_name=_('database name'))
	
	def __unicode__(self):
		return self.name

