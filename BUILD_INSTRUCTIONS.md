# Building Executables for Sphincs ERP + POS

This guide explains how to package the Sphincs ERP and POS applications into standalone executables (.exe files) for Windows.

## Prerequisites

1. **Python 3.10+** installed
2. **All dependencies installed**:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

## Quick Build

Run the automated build script:

```bash
python build_exe.py
```

This will create both executables in the `dist` folder:
- `dist/SphincsERP.exe`
- `dist/SphincsPOS.exe`

## Manual Build

If you prefer to build manually:

### Build ERP:
```bash
pyinstaller --clean erp.spec
```

### Build POS:
```bash
pyinstaller --clean pos.spec
```

## Build Output

- **Executables**: `dist/SphincsERP.exe` and `dist/SphincsPOS.exe`
- **Build files**: `build/` folder (can be deleted after building)
- **Spec files**: `erp.spec` and `pos.spec` (configuration files)

## Distribution

The executables in the `dist` folder are standalone and can be distributed to users. They include:
- All Python dependencies
- PyQt6 libraries
- Application code
- Icons and configuration files

**Note**: 
- The first run will create the database in the user's AppData folder
- The executables are large (100-200MB) because they bundle all dependencies
- Antivirus software may flag PyInstaller executables; this is a false positive

## Troubleshooting

### Missing Modules
If you get import errors, add the missing module to the `hiddenimports` list in the spec file.

### Large File Size
The executables are large because they bundle all dependencies. To reduce size:
- Use `--onefile` mode (already enabled)
- Exclude unused modules in the spec file
- Use UPX compression (already enabled)

### Database Location
The database is created in:
- Windows: `%APPDATA%\Sphincs ERP+POS\sphincs.db`

### Testing
After building, test the executables:
1. Copy to a clean machine (or VM)
2. Run the .exe file
3. Verify all features work correctly

## Advanced Options

### Debug Build
To see console output for debugging, change `console=False` to `console=True` in the spec file.

### Custom Icon
Replace the icon files (`sphincs_icon.ico` and `sphincs_icon_pos.ico`) with your own icons.

### Version Information
Add version information by creating a version file and referencing it in the spec file.

