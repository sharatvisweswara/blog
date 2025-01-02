import tomli
import tomli_w
import yaml
import sys
from pathlib import Path

def convert_config(input_file: str, output_file: str = None) -> None:
    """
    Convert between TOML and YAML configuration files.
    Automatically detects input format based on file extension.
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file {input_file} not found")
    
    # Determine input format from file extension
    input_format = input_path.suffix.lower()[1:]  # Remove the dot
    if input_format not in ['toml', 'yaml', 'yml']:
        raise ValueError(f"Unsupported input format: {input_format}")
    
    # Read input file
    with open(input_file, 'rb' if input_format == 'toml' else 'r') as f:
        if input_format == 'toml':
            data = tomli.load(f)
        else:
            data = yaml.safe_load(f)
    
    # Determine output format and filename
    if output_file is None:
        output_format = 'yaml' if input_format == 'toml' else 'toml'
        output_file = input_path.with_suffix(f'.{output_format}')
    else:
        output_format = Path(output_file).suffix.lower()[1:]
        if output_format not in ['toml', 'yaml', 'yml']:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    # Write output file
    with open(output_file, 'wb' if output_format == 'toml' else 'w') as f:
        if output_format == 'toml':
            tomli_w.dump(data, f)
        else:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True)
    
    print(f"Successfully converted {input_file} to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python config_converter.py input_file [output_file]")
        sys.exit(1)
    
    try:
        convert_config(*sys.argv[1:])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
