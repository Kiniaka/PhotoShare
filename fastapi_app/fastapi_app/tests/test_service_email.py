import pytest
from unittest.mock import patch, AsyncMock
from pydantic import EmailStr
from fastapi_mail import FastMail
from fastapi_app.src.services.email import send_email

@pytest.mark.asyncio
@patch("fastapi_app.src.services.email.FastMail", spec=FastMail)
async def test_send_email(mock_fastmail):
    email = EmailStr("test@example.com")
    username = "testuser"
    host = "localhost"
    
    mock_send_message = AsyncMock()
    mock_fastmail.return_value.send_message = mock_send_message
    
    await send_email(email, username, host)
    
    mock_send_message.assert_called_once()
    call_args = mock_send_message.call_args
    
    assert call_args[1]['template_name'] == "email_template.html"
    
    message = call_args[0][0]
    assert message.subject == "Confirm your email"
    assert message.recipients == [email]
    assert message.template_body["host"] == host
    assert message.template_body["username"] == username
    assert "token" in message.template_body

if __name__ == "__main__":
    pytest.main()