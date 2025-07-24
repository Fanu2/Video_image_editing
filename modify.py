python3 <<EOF
import os, re
repo = "Video_image_editing"
for root, _, files in os.walk(repo):
    for fname in files:
        if fname.endswith(".py"):
            fpath = os.path.join(root, fname)
            with open(fpath, 'r') as f:
                lines = f.readlines()
            new_lines = []
            changed = False
            for line in lines:
                if re.search(r'["\'](/home/|[A-Za-z]:\\\\)', line):
                    new_lines.append(f"# [REMOVED HARDCODED PATH] {line}")
                    changed = True
                else:
                    new_lines.append(line)
            if changed:
                with open(fpath, 'w') as f:
                    f.writelines(new_lines)
                print(f"Cleaned: {fpath}")
EOF

