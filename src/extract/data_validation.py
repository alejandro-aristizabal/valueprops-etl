import toml
import pandera as pa

# Load the configuration file
config = toml.load("./extract/config.toml")


class DynamicSchema:
    @staticmethod
    def from_config(schema_name: str) -> pa.DataFrameSchema:
        schema_config = config['schemas'][schema_name]
        fields = {}

        for field_name, field_config in schema_config.items():
            # Retrieve Pandera data type correctly from the dtypes module or directly from pa
            try:
                if field_config['type'].startswith('Datetime'):
                    # Special handling for datetime types as they need to be instantiated
                    pandera_type = eval(f"pa.{field_config['type']}()")
                else:
                    pandera_type = getattr(pa, field_config['type'])
            except AttributeError:
                raise ValueError(f"Invalid type specified: {field_config['type']}")

            # Prepare checks based on the configuration
            checks = []
            if 'checks' in field_config:
                check_expr = field_config['checks']
                checks.append(pa.Check(lambda x: eval(check_expr), error=f"Check failed: {check_expr}", element_wise=True))

            # Coerce option handling
            coerce = field_config.get('coerce', False)

            # Create the Pandera schema field using the Column constructor
            fields[field_name] = pa.Column(dtype=pandera_type, checks=checks, coerce=coerce)

        # Return a DataFrameSchema with the dynamically created fields
        return pa.DataFrameSchema(fields)
    
            
