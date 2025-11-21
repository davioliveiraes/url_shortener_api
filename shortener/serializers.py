from django.utils import timezone

from rest_framework import serializers

from .models import Click, ShortenedURL


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ["id", "ip_address", "user_agent", "referer", "clicked_at"]
        read_only_fields = fields


class ShortenedURLListSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = ShortenedURL
        fields = [
            "id",
            "short_code",
            "original_url",
            "short_url",
            "is_active",
            "total_clicks",
            "unique_clicks",
            "status",
            "created_at",
        ]

    def get_short_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/r/{obj.short_code}")
        return f"/api/r/{obj.short_code}"

    def get_status(self, obj):
        can_access, message = obj.can_be_accessed()
        return {"can_access": can_access, "message": message}


class ShortenedURLDetailSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    recent_clicks = serializers.SerializerMethodField()

    class Meta:
        model = ShortenedURL
        fields = [
            "id",
            "original_url",
            "short_code",
            "short_url",
            "is_active",
            "expires_at",
            "max_clicks",
            "total_clicks",
            "unique_clicks",
            "qr_code",
            "statistics",
            "status",
            "recent_clicks",
            "created_at",
            "updated_at",
        ]

        read_only_fieds = [
            "short_code",
            "total_clicks",
            "unique_clicks",
            "qr_code",
            "created_at",
            "updated_at",
        ]

    def get_short_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/r/{obj.short_code}")
        return f"/api/r/{obj.short_code}"

    def get_statistics(self, obj):
        return {
            "total_clicks": obj.total_clicks,
            "unique_clicks": obj.unique_clicks,
            "is_expired": obj.is_expired(),
            "has_reached_max_clicks": obj.has_reached_max_clicks(),
        }

    def get_status(self, obj):
        can_access, message = obj.can_be_accessed()
        return {"can_access": can_access, "message": message}

    def get_recent_clicks(self, obj):
        recent = obj.Clicks.all()[:10]
        return ClickSerializer(recent, many=True).data


class ShortenedURLCreateSerializer(serializers.ModelSerializer):
    short_code = serializers.CharField(
        max_length=10,
        required=False,
        allow_blank=True,
        help_text="Custom short code (optional, will be auto-generated if not provided)",
    )

    class Meta:
        model = ShortenedURL
        fields = ["original_url", "short_code", "expires_at", "max_clicks"]

    def validate_short_code(self, value):
        if value:
            if ShortenedURL.objects.filter(short_code=value).exists():
                raise serializers.ValidationError(
                    "Este codigo curto ja esta em uso. Escolha outro."
                )

            if not value.isalnum():
                raise serializers.ValidationError(
                    "Codigo curto deve conter apenas letras e numeros."
                )

            if len(value) < 3:
                raise serializers.ValidationError("Codigo curto deve ter no minimo 3 caracteres.")
        return value

    def validate_expires_at(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError("Data de expiracao deve ser no futuro")
        return value

    def validate_max_clicks(self, value):
        if value is not None and value < 1:
            raise serializers.ValidationError("Numero maximo de cliques deve ser maior que zero.")
        return value

    def create(self, validated_data):
        if not validated_data.get("short_code"):
            import random
            import string

            while True:
                short_code = "".join(random.choices(string.ascii_letters + string.digits, k=6))
                if not ShortenedURL.objects.filter(short_code=short_code):
                    validated_data["short_code"] = short_code
                    break

        return super().create(validated_data)


class ShortenedURLUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ["original_url", "is_active", "expires_at", "max_clicks"]

    def validate_expires_at(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError("Data de expiracao deve ser no futuro.")
        return value

    def validate_max_clicks(self, value):
        if value is not None and value < 1:
            raise serializers.ValidationError("Numero maximo de cliques deve ser maior que zero.")
        return value
