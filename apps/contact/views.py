from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from apps.telegram_bot.utils import send_telegram_notification


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send message to Telegram admin
            message_text = (
                f"<b>New Contact Message</b>\n\n"
                f"<b>Name:</b> {contact_message.name}\n"
                f"<b>Email:</b> {contact_message.email}\n"
                f"<b>Subject:</b> {contact_message.subject}\n"
                f"<b>Message:</b> {contact_message.message}"
            )
            send_telegram_notification(message_text)
            
            messages.success(request, 'پیام شما با موفقیت ارسال شد.')
            return redirect('contact:contact_us')  # Redirect to the same page or a success page
    else:
        form = ContactForm()
    return render(request, 'contact/contact_us.html', {'form': form})
