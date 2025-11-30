from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model


# Obtenemos el modelo actualizado
User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role  # 👈 se incluye el rol
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
            'id': self.user.id,
            # --- NUEVOS CAMPOS EN LA RESPUESTA DE LOGIN ---
            'address': self.user.address,
            'phone': self.user.phone,
        }
        return data    


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role", "address", "phone", "is_staff", "is_active", "notification_channels"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            role=validated_data.get('role', 'cliente'),
            # --- GUARDAMOS LOS NUEVOS DATOS ---
            address=validated_data.get('address', ''),
            phone=validated_data.get('phone', ''),
            # -- nuevo Refactor, canales de notificacion
            notification_channels=validated_data.get('notification_channels', [])
        )
        return user