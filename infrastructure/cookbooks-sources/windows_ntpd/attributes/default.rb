CHARS = ('0'..'9').to_a + ('A'..'Z').to_a + ('a'..'z').to_a
def random_password(length=10)
   CHARS.sort_by { rand }.join[0...length]
end

default["windows_ntpd"]["service_user"] = "ntp"
default["windows_ntpd"]["service_password"] = random_password(12)