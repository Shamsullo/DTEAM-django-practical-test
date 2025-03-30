from rest_framework import serializers
from main.models import CV, Contact, Skill, Project


class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = [
            "id",
            "first_name",
            "last_name",
            "bio",
            "created_at",
            "updated_at",
        ]


class ContactSerializer(serializers.ModelSerializer):
    contact_type_display = serializers.CharField(
        source="get_contact_type_display", read_only=True
    )
    contact_url = serializers.CharField(
        source="get_contact_url", read_only=True
    )
    icon_class = serializers.CharField(source="get_icon_class", read_only=True)

    class Meta:
        model = Contact
        fields = [
            "id",
            "contact_type",
            "contact_type_display",
            "value",
            "is_primary",
            "contact_url",
            "icon_class",
        ]

    def create(self, validated_data):
        validated_data["cv_id"] = self.context["view"].kwargs["cv_pk"]
        return super().create(validated_data)

    def validate(self, data):
        # Check if making a contact primary when another primary exists
        if data.get("is_primary"):
            cv_id = self.context["view"].kwargs.get("cv_pk")
            contact_type = data.get("contact_type")
            existing_primary = Contact.objects.filter(
                cv_id=cv_id, contact_type=contact_type, is_primary=True
            )

            # Exclude current instance in case of update
            if self.instance:
                existing_primary = existing_primary.exclude(
                    id=self.instance.id
                )

            if existing_primary.exists():
                raise serializers.ValidationError(
                    f"A primary {contact_type} contact already exists for this CV"
                )

        return data


class SkillSerializer(serializers.ModelSerializer):
    proficiency_display = serializers.CharField(
        source="get_proficiency_display", read_only=True
    )

    class Meta:
        model = Skill
        fields = ["id", "name", "proficiency", "proficiency_display"]

    def create(self, validated_data):
        validated_data["cv_id"] = self.context["view"].kwargs["cv_pk"]
        return super().create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "url",
            "duration",
        ]

    def create(self, validated_data):
        validated_data["cv_id"] = self.context["view"].kwargs["cv_pk"]
        return super().create(validated_data)

    def get_duration(self, obj):
        if not obj.end_date:
            return "Ongoing"
        duration = obj.end_date - obj.start_date
        return f"{duration.days} days"


class CVDetailSerializer(CVSerializer):
    """Serializer for detailed CV view with all related data"""

    contacts = ContactSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = CV
        fields = [
            "id",
            "first_name",
            "last_name",
            "bio",
            "created_at",
            "updated_at",
            "contacts",
            "skills",
            "projects",
        ]
