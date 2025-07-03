from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def upload_to_drive(filepath, filename):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth)

    # Buscar la carpeta ITFFF
    folder_name = 'ITFFF'
    query = f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    folder_list = drive.ListFile({'q': query}).GetList()
    
    # Si la carpeta no existe, crearla
    if not folder_list:
        folder = drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
        folder.Upload()
        folder_id = folder['id']
    else:
        folder_id = folder_list[0]['id']

    # Subir el archivo a la carpeta
    file = drive.CreateFile({
        'title': filename,
        'parents': [{'id': folder_id}]
    })
    file.SetContentFile(filepath)
    file.Upload()
    print(f"✅ Imagen subida a Google Drive en la carpeta '{folder_name}': {filename}")