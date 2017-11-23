from rest_framework import serializers

class PartySerializer(serializers.Serializer):

    # Required
    addresses = serializers.ListField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()

    # Optional
    about = serializers.CharField(allow_null=True, allow_blank=True)
    title = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    jobTitle = serializers.CharField(allow_null=True, allow_blank=True)

    organisation = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    phoneNumbers = serializers.ListField()
    websites = serializers.ListField()
    pictureURL = serializers.CharField(allow_null=True, allow_blank=True)
    owner = serializers.CharField(allow_null=True, allow_blank=True)
    emailAddresses = serializers.ListField()
    # [{u'type': None, u'id': 293627793, u'address': u'massimo.santoli@top-ix.org'}

    type = serializers.CharField(allow_null=True, allow_blank=True)
    id = serializers.IntegerField()

    # createdAt = serializers.DateField(allow_null=True, blank=True, format="%Y-%m-%dT%H:%M:%SZ")
    # updatedAt = serializers.DateField(allow_null=True, blank=True, format="%Y-%m-%dT%H:%M:%SZ")
    # lastContactedAt = serializers.DateField(allow_null=True, blank=True, format="%Y-%m-%dT%H:%M:%SZ")
    createdAt = serializers.CharField(allow_null=True)
    updatedAt = serializers.CharField(allow_null=True)
    lastContactedAt = serializers.CharField(allow_null=True)

