class Macprefs < Formula
  desc "Backup and Restore your Mac System and App Preferences"
  homepage "https://github.com/clintmod/macprefs"
  url "https://github.com/clintmod/macprefs/archive/###version###.tar.gz"
  sha256 "###sha256###"

  depends_on "python@3.13"

  def install
    libexec.install Dir["src/*"]
    bin.write_exec_script libexec/"macprefs"
  end

  test do
    system "#{bin}/macprefs", "--help"
  end
end
