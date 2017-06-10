"""
    PyWpBackup: a tool to backup wordpress database and directory.
    Copyright (C) <2017>  <Michal (makyox dot aubert at gmail do com)>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import optparse
import os
import datetime
import shutil
import re
from subprocess import Popen, PIPE
 
date = datetime.datetime.now().strftime('%Y%m%d-%s')
f_date = datetime.datetime.now().strftime('%Y%m%d')
 
define_pattern = re.compile(r"""\bdefine\(\s*('|")(.*)\1\s*,\s*('|")(.*)\3\)\s*;""")
assign_pattern = re.compile(r"""(^|;)\s*\$([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)\s*=\s*('|")(.*)\3\s*;""")

php_vars = {}
for line in open("wordpress/wp-config.php"):
  for match in define_pattern.finditer(line):
    php_vars[match.group(2)]=match.group(4)
  for match in assign_pattern.finditer(line):
    php_vars[match.group(2)]=match.group(4)


def backup_all_databases():
    args = ['mysqldump', php_vars['DB_NAME'], '-u', php_vars['DB_USER'], '-p'+php_vars['DB_PASSWORD']]
    with open("%s.sql.gz" % f_date, 'wb') as f:
        p1 = Popen(args, stdout=PIPE)
        p2 = Popen('gzip', stdin=p1.stdout, stdout=f)
        p1.stdout.close()
        p2.wait()
        p1.wait()
 
def tar_html_folder():
    output_filename_1 = "%s.html_dir"  % f_date
    output_filename_2 = "%s.html_dir.zip"  % f_date
    dir_name = 'wordpress/'
    dst = "%s" % date
    shutil.make_archive(output_filename_1, 'zip', dir_name)
    shutil.move(output_filename_2, dst)
 
def main():
    archive_path = "%s" % date
    os.mkdir(archive_path, 0755)
    backup_all_databases()
    src_file = "%s.sql.gz" % f_date
    dst = "%s" % date
    shutil.move(src_file, dst)
    tar_html_folder()

if __name__ == "__main__":
    main()