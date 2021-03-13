# set up the default terminal
ENV["TERM"]="linux"

Vagrant.configure("2") do |config|
  
  # set the image for the vagrant box
  config.vm.box = "opensuse/Leap-15.2.x86_64"
  ## Set the image version
  # config.vm.box_version = "15.2.31.247"

  # st the static IP for the vagrant box
  config.vm.network "private_network", ip: "192.168.50.4"
  config.vm.network "forwarded_port", guest: 3111, host: 3111
  config.vm.network "forwarded_port", guest: 7111, host: 7111
  config.vm.network "forwarded_port", guest: 4111, host: 4111
  config.vm.network "forwarded_port", guest: 5111, host: 5111

  # consifure the parameters for VirtualBox provider
  config.vm.provider "virtualbox" do |vb|
    vb.gui = true
    vb.memory = "4096"
    vb.cpus = 4
    vb.name = "techtrends-vm"
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end
end
