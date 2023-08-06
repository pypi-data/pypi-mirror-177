import os
import json
import requests
import sys
import click
from pathlib import Path

from stochasticx.constants.urls import LOGIN_URL, TOKEN_AUTH_PATH
from stochasticx.constants.urls import ME_URL


class LoginUtils:
    @staticmethod
    def login_request(username, password):
        """Private method to do the login request

        Args:
            username (str): username
            password (str): password

        Returns:
            str: token
        """
        login_info = {"email": username, "password": password}

        response = requests.post(LOGIN_URL, data=login_info)
        try:
            response.raise_for_status()
        except:
            click.secho(
                "[+] Your credentials are incorrect.\n", 
                fg='red', 
                bold=True
            )
            sys.exit()

        response_data = response.json()
        token = response_data["token"]
        
        # Save token in ENV var
        os.environ["STOCHASTIC_TOKEN"] = token
        
        # Save token in a file
        token_path = Path(TOKEN_AUTH_PATH).resolve()
        
        if not token_path.exists():
            token_path.parent.mkdir(parents=True, exist_ok=True)
            
        with open(str(token_path), 'w', encoding='utf-8') as f:
            json.dump({
                "token": token
            }, f, ensure_ascii=False, indent=4)
        
        return token

class AuthUtils:
    
    @staticmethod
    def get_auth_headers():
        """Get authentication headers from the webapp

        Raises:
            ValueError: if token not found in the following ENV variable STOCHASTIC_TOKEN

        Returns:
            dict: auth headers
        """
        token = os.getenv("STOCHASTIC_TOKEN")
        
        if token is None:
            if Path(TOKEN_AUTH_PATH).exists():
                f = open(TOKEN_AUTH_PATH)
                data = json.load(f)
                token = data['token']

        if token is not None:
            try:
                response = requests.get(
                    ME_URL, 
                    headers={
                        'Authorization': 'Bearer ' + token
                    }
                )
                response.raise_for_status()
            except:
                click.secho(
                    "[+] You are not logged in. Please execute:", 
                    fg='red', 
                    bold=True
                )
                click.secho(
                    "\n     stochasticx login \n",
                    bold=True
                )

                sys.exit()
        
        else:
            click.secho(
                "[+] You are not logged in. Please try:", 
                fg='red', 
                bold=True
            )
            click.secho(
                "\n     stochasticx login \n",
                bold=True
            )
            click.secho("[+] You can sign up for a free account at: https://app.stochastic.ai/signup")

            sys.exit()

        return {
            'Authorization': 'Bearer ' + token
        }    