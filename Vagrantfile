# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.synced_folder ".", "/home/vagrant/project"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "3512"
    vb.name = "dev.collegesearch.co"
  end

  config.vm.provision "shell", path: "provision/install.sh"
end