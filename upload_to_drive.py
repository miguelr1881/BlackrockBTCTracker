from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

def upload_to_drive(filepath, filename, current_btc):
    # ------------------ AUTENTICACIÓN ------------------
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

    # ------------------ BUSCAR LA CARPETA IFTTT ------------------
    folder_name = 'IFTTT'
    query = f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    folder_list = drive.ListFile({'q': query}).GetList()

    # Si la carpeta no existe, crearla
    if not folder_list:
        folder = drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
        folder.Upload()
        folder_id = folder['id']
    else:
        folder_id = folder_list[0]['id']

    # ------------------ BUSCAR Y LEER EL last_value.txt ------------------
    txt_filename = 'last_value.txt'
    query_txt = f"title='{txt_filename}' and '{folder_id}' in parents and trashed=false"
    txt_list = drive.ListFile({'q': query_txt}).GetList()

    last_btc = None
    if txt_list:
        txt_file = txt_list[0]
        txt_file.GetContentFile(txt_filename)
        with open(txt_filename, 'r') as f:
            last_btc = f.read().strip()
        os.remove(txt_filename)  # Limpieza del archivo local temporal

    # ------------------ COMPARAR VALORES ------------------
    if str(current_btc) == last_btc:
        print("🔁 No change in BTC holdings. Skipping upload.")
        return "No change"

    print(f"✅ BTC changed from {last_btc} to {current_btc}. Proceeding to upload.")

    # ------------------ ACTUALIZAR last_value.txt ------------------
    with open(txt_filename, 'w') as f:
        f.write(str(current_btc))

    # Subir el nuevo txt al Drive (sobrescribiendo si ya existe)
    file_metadata = {'title': txt_filename, 'parents': [{'id': folder_id}]}
    if txt_list:
        txt_file = txt_list[0]
        txt_file.SetContentFile(txt_filename)
    else:
        txt_file = drive.CreateFile(file_metadata)
        txt_file.SetContentFile(txt_filename)
    txt_file.Upload()
    os.remove(txt_filename)  # Limpieza del archivo local temporal

    print(f"✅ Archivo '{txt_filename}' actualizado en Google Drive.")

    # ------------------ SUBIR LA IMAGEN ------------------
    file = drive.CreateFile({
        'title': filename,
        'parents': [{'id': folder_id}]
    })
    file.SetContentFile(filepath)
    file.Upload()

    print(f"✅ Imagen subida a Google Drive en la carpeta '{folder_name}': {filename}")

    return "Uploaded"
