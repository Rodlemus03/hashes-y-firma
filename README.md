# Laboratorio: Hashes y Firma Digital

## Archivos principales

- `lab_utils.py`: funciones compartidas del laboratorio.
- `explorar_hashes.py`: compara algoritmos hash con dos cadenas parecidas.
- `consultar_hibp.py`: consulta contraseñas filtradas con Have I Been Pwned.
- `demo_passwords.py`: muestra almacenamiento seguro con Argon2id.
- `demo_hmac.py`: muestra el uso de HMAC-SHA256.
- `generar_manifiesto.py`: genera el archivo `SHA256SUMS.txt`.
- `verificar_paquete.py`: verifica archivos contra el manifiesto.
- `generar_claves_rsa.py`: genera claves RSA.
- `firmar_manifiesto.py`: firma el manifiesto.
- `verificar_firma.py`: valida la firma del manifiesto.

## Requisitos

- Python 3.12 o compatible  
- `pip`

## Instalación

```bash
python -m pip install -r requirements.txt
```

Si prefieres usar entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Uso

### 1. Explorar hashes

```bash
python explorar_hashes.py
```

### 2. Consultar contraseñas filtradas

```bash
python consultar_hibp.py
```

### 3. Probar Argon2id

```bash
python demo_passwords.py medisoft2024
```

### 4. Probar HMAC-SHA256

```bash
python demo_hmac.py
```

### 5. Generar y verificar manifiesto

```bash
python generar_manifiesto.py sample_package/app.exe sample_package/config.ini sample_package/device_map.json sample_package/driver.sys sample_package/release_notes.txt
python verificar_paquete.py --base-dir sample_package
```

### 6. Firmar y verificar manifiesto

```bash
python generar_claves_rsa.py
python firmar_manifiesto.py
python verificar_firma.py
```

## Estructura

```text
lab_utils.py
sample_package/
```

---

## Preguntas y respuestas

### ¿Cuántos bits cambiaron entre los dos SHA-256?

Cambiaron **120 bits de 256**.  
Esto demuestra el **efecto avalancha**, donde un cambio pequeño en la entrada produce un cambio grande en la salida.

---

### ¿Por qué MD5 es inseguro para integridad?

MD5 ya no es seguro porque existen **colisiones conocidas**.  
Esto significa que dos archivos distintos pueden producir el mismo hash, por lo que no es confiable para verificar integridad.

---

### ¿Por qué SHA-256 directo sobre contraseñas es inseguro?

Porque es **rápido y predecible**, lo que facilita ataques de **fuerza bruta y diccionario**.  

Para contraseñas se debe usar un algoritmo especializado como **Argon2id con salt**.

---

### ¿Por qué la firma sigue siendo válida si altero un archivo de datos?

Porque la firma protege el contenido del archivo **`SHA256SUMS.txt`**, no cada archivo individual directamente.  

Si el manifiesto no cambia, la firma sigue siendo válida.

---

### ¿Qué sucede al ejecutar `verificar_paquete.py` después de alterar un archivo?

El archivo modificado aparece como **alterado**, ya que su hash no coincide con el valor almacenado en el manifiesto.

---

### ¿Qué ocurre si se altera el manifiesto firmado?

La firma deja de ser válida, porque el contenido firmado ya no coincide con el original.
