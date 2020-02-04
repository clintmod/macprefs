class Macprefs < Formula
    include Language::Python::Virtualenv
  
    desc "Backup and Restore your Mac System and App Preferences"
    homepage "https://github.com/clintmod/macprefs"
    url "https://github.com/clintmod/macprefs/archive/###version###.tar.gz"
    sha256 "###sha256###"
  
    depends_on :python3
  
    def install
      bin.install Dir["*"]
    end
  
    test do
      system "#{bin}/macprefs", "--help"
    end
  end
  