INSERT INTO air_quality_parameters (
    parameter_name, unit
) VALUES (
    %(parameter_name)s, %(unit)s
) ON CONFLICT (parameter_name) DO NOTHING;
