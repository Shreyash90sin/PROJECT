import requests

def upload_to_ipfs(file_path: str, pinata_jwt: str) -> str:
    headers = {'Authorization': f'Bearer {pinata_jwt}'}
    with open(file_path, 'rb') as f:
        response = requests.post(
            'https://api.pinata.cloud/pinning/pinFileToIPFS',
            files={'file': f},
            headers=headers
        )
    return response.json()['IpfsHash']
