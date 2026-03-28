from django.core.mail import send_mail
from django.conf import settings

class EmailService:
    
    @staticmethod
    def send_validation_email(stand, password):
        """Envoie un email au propriétaire avec le mot de passe du stand"""
        subject = f"✅ Validation de votre stand - {stand.nom}"
        
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .password {{ font-size: 24px; font-weight: bold; text-align: center; padding: 20px; background: #f5f5f5; border-radius: 5px; margin: 20px 0; letter-spacing: 2px; }}
                .footer {{ text-align: center; font-size: 12px; color: #666; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Xobo Ticket</h1>
                    <p>Plateforme de gestion des stands</p>
                </div>
                <div style="padding: 20px;">
                    <h2>Bonjour {stand.prenom_prop} {stand.nom_prop},</h2>
                    <p>Votre stand <strong>"{stand.nom}"</strong> a été validé par notre équipe !</p>
                    <p>Voici vos identifiants de connexion :</p>
                    <div class="password">
                        🔑 Mot de passe : <strong>{password}</strong>
                    </div>
                    <p>Email du stand : <strong>{stand.email}</strong></p>
                    <p>Numéro de stand : <strong>{stand.numero_stand}</strong></p>
                    <div style="text-align: center; margin: 20px 0;">
                        <a href="{settings.FRONTEND_URL}/stand-login" style="background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                            Se connecter à mon stand
                        </a>
                    </div>
                    <p><strong>⚠️ Important :</strong> Gardez ce mot de passe précieusement.</p>
                </div>
                <div class="footer">
                    <p>© 2024 Xobo Ticket - Gestion de stands</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_message = f"""
        Bonjour {stand.prenom_prop} {stand.nom_prop},
        
        Votre stand "{stand.nom}" a été validé !
        
        Identifiants de connexion:
        - Email: {stand.email}
        - Mot de passe: {password}
        - Numéro: {stand.numero_stand}
        
        Connectez-vous sur: {settings.FRONTEND_URL}/stand-login
        
        Cordialement,
        L'équipe Xobo Ticket
        """
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[stand.email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"✅ Email envoyé à {stand.email}")
            return True
        except Exception as e:
            print(f"❌ Erreur d'envoi: {e}")
            return False

    @staticmethod
    def send_temp_password_email(stand, temp_password):
        """Envoie un email au propriétaire avec le mot de passe temporaire"""
        subject = f"🔐 Validation de votre stand - {stand.nom}"
        
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .password {{ font-size: 24px; font-weight: bold; text-align: center; padding: 20px; background: #f5f5f5; border-radius: 5px; margin: 20px 0; letter-spacing: 2px; }}
                .button {{ display: inline-block; padding: 12px 24px; background: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; font-size: 12px; color: #666; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Xobo Ticket</h1>
                    <p>Validation de votre stand</p>
                </div>
                <div style="padding: 20px;">
                    <h2>Bonjour {stand.prenom_prop} {stand.nom_prop},</h2>
                    <p>Votre stand <strong>"{stand.nom}"</strong> a été examiné par notre équipe.</p>
                    <p>Pour <strong>activer</strong> votre stand, veuillez utiliser le mot de passe ci-dessous :</p>
                    <div class="password">
                        🔑 <strong>{temp_password}</strong>
                    </div>
                    <p>Ce mot de passe vous permettra d'accéder à votre espace stand.</p>
                    <div style="text-align: center;">
                        <a href="{settings.FRONTEND_URL}/activate-stand/{stand.id}" class="button">
                            Activer mon stand
                        </a>
                    </div>
                    <p><strong>⚠️ Important :</strong> Une fois activé, vous pourrez modifier ce mot de passe.</p>
                </div>
                <div class="footer">
                    <p>© 2024 Xobo Ticket - Gestion de stands</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_message = f"""
        Bonjour {stand.prenom_prop} {stand.nom_prop},
        
        Votre stand "{stand.nom}" a été validé par l'administrateur.
        
        Pour activer votre stand, utilisez le mot de passe : {temp_password}
        
        Activez votre stand ici : {settings.FRONTEND_URL}/activate-stand/{stand.id}
        
        Cordialement,
        L'équipe Xobo Ticket
        """
        
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[stand.email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"✅ Email envoyé à {stand.email}")
            return True
        except Exception as e:
            print(f"❌ Erreur d'envoi: {e}")
            return False
