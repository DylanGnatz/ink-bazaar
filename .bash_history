psql --version
sudo apt-get install postgresql-12
sudo apt-get update
sudo apt-get install postgresql-12
sudo apt -y install vim bash-completion wget
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
sudo apt update
sudo apt -y install postgresql-12 postgresql-client-12
systemctl status postgresql.service 
sudo su - postgres
psql --version
psql -U dlg2178 -h 35.196.192.139 -d proj1part2
ALTER USER <uni> WITH PASSWORD '<new password>'; 
psql -U dlg2178 -h 35.196.192.139 -d proj1part2
psql -h 35.196.192.139 -U [your_partner's_uni] proj1part2 -f db.sql
psql -h 35.196.192.139 -U dlg2178 proj1part2 -f db.sql
psql -h 35.196.192.139 -U [your_partner's_uni] proj1part2 -f db.sql
psql -h 35.196.192.139 -U dlg2178  proj1part2 -f db.sql
psql -U <uni> -h 35.196.192.139 -d proj1part2
psql -U dlg2178 -h 35.196.192.139 -d proj1part2
