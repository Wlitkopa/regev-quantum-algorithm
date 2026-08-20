def convert_to_matrix_row(output_data) -> str:
    """Human-readable rendering of the ``output_data`` structure.

    Each entry has the shape ``[vector, raw_bits, shot_count]``; the returned
    string lists every vector on its own line, prefixed by the shot count.
    """
    lines: list[str] = []
    for entry in output_data:
        vec_str = ", ".join(str(v) for v in entry[0])
        lines.append(f"\nvector with {entry[2]} shots: [{vec_str}],")
    return "".join(lines)
