#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ListGenerateX - Ultimate Wordlist Generator
GitHub: [Your Repository]
Author: [Your Name]
Version: 2.0

YASAL UYARI: Bu araç sadece yasal ve etik amaçlar için kullanılmalıdır.
Yalnızca kendi sistemlerinizde veya yazılı izin alınmış sistemlerde kullanın.
"""

import os
import sys
import itertools
from datetime import datetime
from pathlib import Path

class Colors:
    """Terminal renkleri"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ListGenerateX:
    def __init__(self):
        # Kullanıcı verileri
        self.first_name = ""
        self.last_name = ""
        self.nickname = ""
        self.birth_date = ""
        self.birth_place = ""
        self.phone = ""
        self.father_name = ""
        self.mother_name = ""
        self.spouse_name = ""
        self.child_name = ""
        self.pet_name = ""
        self.company = ""
        self.school = ""
        self.hobby = ""
        self.favorite_team = ""
        self.favorite_color = ""
        self.lucky_number = ""
        self.custom_words = []
       
        # Ayarlar
        self.min_length = 6
        self.max_length = 16
        self.use_special = True
        self.output_file = ""
       
        # Kelime listesi
        self.wordlist = set()
       
        # Leet speak tablosu
        self.leet_map = {
            'a': ['a', '4', '@', 'A'],
            'e': ['e', '3', 'E'],
            'i': ['i', '1', '!', 'I', '|'],
            'o': ['o', '0', 'O'],
            's': ['s', '5', '$', 'S'],
            't': ['t', '7', 'T', '+'],
            'l': ['l', '1', 'L', '|'],
            'g': ['g', '9', 'G'],
            'b': ['b', '8', 'B'],
            'z': ['z', '2', 'Z']
        }
       
        self.special_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '_', '-', '.', '~']
        self.common_suffixes = ['123', '1234', '12345', '321', '69', '420', '2024', '2025']
   
    def print_banner(self):
        """Başlık göster"""
        banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║               {Colors.BOLD}██╗     ██╗███████╗████████╗ ██████╗ ███████╗███╗   ██╗{Colors.END}{Colors.CYAN}        ║
║               {Colors.BOLD}██║     ██║██╔════╝╚══██╔══╝██╔════╝ ██╔════╝████╗  ██║{Colors.END}{Colors.CYAN}        ║
║               {Colors.BOLD}██║     ██║███████╗   ██║   ██║  ███╗█████╗  ██╔██╗ ██║{Colors.END}{Colors.CYAN}        ║
║               {Colors.BOLD}██║     ██║╚════██║   ██║   ██║   ██║██╔══╝  ██║╚██╗██║{Colors.END}{Colors.CYAN}        ║
║               {Colors.BOLD}███████╗██║███████║   ██║   ╚██████╔╝███████╗██║ ╚████║{Colors.END}{Colors.CYAN}        ║
║               {Colors.BOLD}╚══════╝╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝{Colors.END}{Colors.CYAN}        ║
║                                                              ║
║               {Colors.GREEN}Ultimate Wordlist Generator v2.0{Colors.END}{Colors.CYAN}                   ║
║               {Colors.YELLOW}The Most Powerful Wordlist Tool{Colors.END}{Colors.CYAN}                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.RED}{Colors.BOLD}⚠️  YASAL UYARI ⚠️{Colors.END}
{Colors.YELLOW}Bu araç sadece yasal ve etik amaçlar için kullanılmalıdır.
Yalnızca kendi sistemlerinizde veya yazılı izin alınmış sistemlerde kullanın.
Yetkisiz erişim girişimleri yasalara aykırıdır ve cezai sorumluluk doğurur.{Colors.END}

"""
        print(banner)
   
    def get_input(self, prompt, default=""):
        """Kullanıcıdan veri al"""
        if default:
            user_input = input(f"{Colors.CYAN}{prompt} [{default}]: {Colors.END}").strip()
            return user_input if user_input else default
        else:
            user_input = input(f"{Colors.CYAN}{prompt}: {Colors.END}").strip()
            return user_input
   
    def setup(self):
        """Başlangıç ayarları"""
        print(f"\n{Colors.GREEN}═══ AYARLAR ═══{Colors.END}\n")
       
        # Kayıt yeri
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        output_path = self.get_input("Kelime listesi nereye kaydedilsin? (Enter = Masaüstü)", desktop)
       
        if not os.path.exists(output_path):
            print(f"{Colors.RED}[!] Belirtilen klasör bulunamadı, masaüstü kullanılıyor.{Colors.END}")
            output_path = desktop
       
        filename = self.get_input("Dosya adı", "wordlist.txt")
        if not filename.endswith('.txt'):
            filename += '.txt'
       
        self.output_file = os.path.join(output_path, filename)
       
        # Uzunluk ayarları
        print(f"\n{Colors.YELLOW}Parola uzunluk aralığı (En az: 6, En fazla: 16){Colors.END}")
       
        min_input = self.get_input("Minimum uzunluk (Enter = 6)", "6")
        try:
            self.min_length = max(int(min_input), 6)
        except:
            self.min_length = 6
       
        max_input = self.get_input("Maximum uzunluk (Enter = 16)", "16")
        try:
            self.max_length = min(int(max_input), 16)
        except:
            self.max_length = 16
       
        if self.min_length > self.max_length:
            self.min_length, self.max_length = self.max_length, self.min_length
       
        print(f"{Colors.GREEN}[✓] Uzunluk: {self.min_length}-{self.max_length} karakter{Colors.END}")
   
    def collect_data(self):
        """Kullanıcı verilerini topla"""
        print(f"\n{Colors.GREEN}═══ KİŞİSEL BİLGİLER ═══{Colors.END}")
        print(f"{Colors.YELLOW}(Boş geçmek için Enter tuşuna basın){Colors.END}\n")
       
        self.first_name = self.get_input("İsim")
        self.last_name = self.get_input("Soyisim")
        self.nickname = self.get_input("Takma ad / Kullanıcı adı")
       
        print(f"\n{Colors.GREEN}═══ TARİHLER ═══{Colors.END}\n")
        self.birth_date = self.get_input("Doğum tarihi (gg/aa/yyyy veya gg-aa-yyyy)")
       
        print(f"\n{Colors.GREEN}═══ YERLER ═══{Colors.END}\n")
        self.birth_place = self.get_input("Doğum yeri")
       
        print(f"\n{Colors.GREEN}═══ İLETİŞİM ═══{Colors.END}\n")
        self.phone = self.get_input("Telefon numarası (son 4-10 hane)")
       
        print(f"\n{Colors.GREEN}═══ AİLE ═══{Colors.END}\n")
        self.father_name = self.get_input("Baba adı")
        self.mother_name = self.get_input("Anne adı")
        self.spouse_name = self.get_input("Eş adı")
        self.child_name = self.get_input("Çocuk adı")
       
        print(f"\n{Colors.GREEN}═══ DİĞER ═══{Colors.END}\n")
        self.pet_name = self.get_input("Evcil hayvan adı")
        self.company = self.get_input("Şirket / İş yeri")
        self.school = self.get_input("Okul adı")
        self.hobby = self.get_input("Hobi / İlgi alanı")
        self.favorite_team = self.get_input("Favori takım")
        self.favorite_color = self.get_input("Favori renk")
        self.lucky_number = self.get_input("Şanslı sayı")
       
        print(f"\n{Colors.GREEN}═══ EK KELİMELER ═══{Colors.END}")
        print(f"{Colors.YELLOW}Özel kelimeler eklemek için yazıp Enter'a basın (Bitirmek için boş Enter){Colors.END}\n")
       
        while True:
            word = self.get_input("Kelime")
            if not word:
                break
            self.custom_words.append(word)
            print(f"{Colors.GREEN}[+] Eklendi: {word}{Colors.END}")
       
        # Özel karakterler
        print(f"\n{Colors.GREEN}═══ AYARLAR ═══{Colors.END}\n")
        special = self.get_input("Özel karakterler eklensin mi? (e/h)", "e").lower()
        self.use_special = special == 'e'
   
    def leet_transform(self, word, max_variations=100):
        """Leet speak dönüşümleri"""
        variations = [word]
       
        for char, replacements in self.leet_map.items():
            if char.lower() not in word.lower():
                continue
           
            new_variations = []
            for variation in variations[:max_variations]:
                for replacement in replacements:
                    new_var = variation.replace(char, replacement)
                    new_var2 = variation.replace(char.upper(), replacement)
                    new_variations.extend([new_var, new_var2])
           
            variations.extend(new_variations[:max_variations])
            if len(variations) > max_variations:
                variations = variations[:max_variations]
       
        return list(set(variations))
   
    def generate_variations(self, word):
        """Kelime varyasyonları üret"""
        if not word:
            return []
       
        variations = set()
       
        # Orijinal
        variations.add(word)
       
        # Büyük/küçük harf
        variations.add(word.lower())
        variations.add(word.upper())
        variations.add(word.capitalize())
        variations.add(word.title())
       
        # Ters
        variations.add(word[::-1])
        variations.add(word[::-1].capitalize())
       
        # Leet speak
        leet_vars = self.leet_transform(word)
        variations.update(leet_vars[:50])
       
        return list(variations)
   
    def process_dates(self):
        """Tarih işleme"""
        dates = []
       
        if not self.birth_date:
            return dates
       
        try:
            # Farklı formatları dene
            for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y', '%Y-%m-%d', '%Y/%m/%d']:
                try:
                    date_obj = datetime.strptime(self.birth_date, fmt)
                   
                    # Tüm formatlar
                    dates.extend([
                        date_obj.strftime('%d%m%Y'),    # 01011990
                        date_obj.strftime('%d%m%y'),    # 010190
                        date_obj.strftime('%Y%m%d'),    # 19900101
                        date_obj.strftime('%y%m%d'),    # 900101
                        date_obj.strftime('%Y'),        # 1990
                        date_obj.strftime('%y'),        # 90
                        date_obj.strftime('%d%m'),      # 0101
                        date_obj.strftime('%m%d'),      # 0101
                        date_obj.strftime('%m%y'),      # 0190
                        date_obj.strftime('%d'),        # 01
                        date_obj.strftime('%m'),        # 01
                    ])
                    break
                except:
                    continue
        except:
            # Sadece rakamları al
            digits = ''.join(filter(str.isdigit, self.birth_date))
            if digits:
                dates.extend([
                    digits,
                    digits[:4],
                    digits[:6],
                    digits[-4:],
                    digits[-2:]
                ])
       
        return list(set(dates))
   
    def generate_wordlist(self):
        """Ana kelime listesi oluşturma"""
        print(f"\n{Colors.GREEN}═══ KELİME LİSTESİ OLUŞTURULUYOR ═══{Colors.END}\n")
       
        # Tüm kelimeleri topla
        all_words = []
       
        fields = [
            self.first_name, self.last_name, self.nickname,
            self.birth_place, self.father_name, self.mother_name,
            self.spouse_name, self.child_name, self.pet_name,
            self.company, self.school, self.hobby,
            self.favorite_team, self.favorite_color
        ]
       
        for field in fields:
            if field:
                all_words.extend(self.generate_variations(field))
       
        # Özel kelimeler
        for word in self.custom_words:
            all_words.extend(self.generate_variations(word))
       
        print(f"{Colors.YELLOW}[~] Temel kelimeler oluşturuldu: {len(set(all_words))}{Colors.END}")
       
        # Sayılar
        numbers = []
        if self.phone:
            phone_digits = ''.join(filter(str.isdigit, self.phone))
            if phone_digits:
                numbers.extend([
                    phone_digits,
                    phone_digits[-4:],
                    phone_digits[-6:],
                    phone_digits[-8:],
                    phone_digits[:4],
                ])
       
        if self.lucky_number:
            numbers.append(self.lucky_number)
       
        # Tarihler
        numbers.extend(self.process_dates())
        numbers.extend(self.common_suffixes)
       
        numbers = list(set(numbers))
        print(f"{Colors.YELLOW}[~] Sayı varyasyonları: {len(numbers)}{Colors.END}")
       
        # Temel kelimeleri ekle
        self.wordlist.update(all_words)
        self.wordlist.update(numbers)
       
        # Kombinasyonlar
        print(f"{Colors.YELLOW}[~] Kombinasyonlar oluşturuluyor...{Colors.END}")
       
        base_words = list(set(all_words))[:100]
       
        # Kelime + Sayı
        for word in base_words:
            for num in numbers:
                self.wordlist.add(f"{word}{num}")
                self.wordlist.add(f"{num}{word}")
                self.wordlist.add(f"{word}_{num}")
                self.wordlist.add(f"{word}.{num}")
                self.wordlist.add(f"{word}-{num}")
               
                if self.use_special:
                    self.wordlist.add(f"{word}{num}!")
                    self.wordlist.add(f"{word}@{num}")
                    self.wordlist.add(f"{word}#{num}")
                    self.wordlist.add(f"{word}${num}")
       
        # İki kelime kombinasyonu
        for i, word1 in enumerate(base_words[:50]):
            for word2 in base_words[i+1:51]:
                self.wordlist.add(f"{word1}{word2}")
                self.wordlist.add(f"{word1}_{word2}")
                self.wordlist.add(f"{word1}.{word2}")
                self.wordlist.add(f"{word2}{word1}")
       
        # Üç elemanlı kombinasyonlar
        if self.first_name and self.last_name:
            for num in numbers[:20]:
                base = [
                    f"{self.first_name}{self.last_name}",
                    f"{self.last_name}{self.first_name}",
                    f"{self.first_name.lower()}{self.last_name.lower()}",
                ]
                for b in base:
                    self.wordlist.add(f"{b}{num}")
                    if self.use_special:
                        for char in self.special_chars[:5]:
                            self.wordlist.add(f"{b}{num}{char}")
                            self.wordlist.add(f"{b}{char}{num}")
       
        # Özel karakter kombinasyonları
        if self.use_special:
            print(f"{Colors.YELLOW}[~] Özel karakterler ekleniyor...{Colors.END}")
            special_words = set()
            for word in list(self.wordlist)[:1000]:
                for char in self.special_chars[:8]:
                    special_words.add(f"{word}{char}")
                    special_words.add(f"{char}{word}")
            self.wordlist.update(special_words)
       
        # Uzunluk filtresi
        print(f"{Colors.YELLOW}[~] Filtreleme yapılıyor...{Colors.END}")
        self.wordlist = {
            word for word in self.wordlist
            if self.min_length <= len(word) <= self.max_length
        }
       
        print(f"{Colors.GREEN}[✓] Toplam kelime: {len(self.wordlist)}{Colors.END}")
   
    def save_wordlist(self):
        """Kelime listesini kaydet"""
        print(f"\n{Colors.YELLOW}[~] Dosyaya kaydediliyor...{Colors.END}")
       
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                for word in sorted(self.wordlist):
                    f.write(word + '\n')
           
            file_size = os.path.getsize(self.output_file) / 1024
           
            print(f"\n{Colors.GREEN}{'═' * 60}{Colors.END}")
            print(f"{Colors.GREEN}{Colors.BOLD}[✓] BAŞARIYLA TAMAMLANDI!{Colors.END}")
            print(f"{Colors.GREEN}{'═' * 60}{Colors.END}")
            print(f"{Colors.CYAN}Dosya: {Colors.END}{self.output_file}")
            print(f"{Colors.CYAN}Toplam Kelime: {Colors.END}{len(self.wordlist):,}")
            print(f"{Colors.CYAN}Dosya Boyutu: {Colors.END}{file_size:.2f} KB")
            print(f"{Colors.GREEN}{'═' * 60}{Colors.END}\n")
           
        except Exception as e:
            print(f"{Colors.RED}[!] Hata: {e}{Colors.END}")
   
    def show_preview(self):
        """Önizleme göster"""
        preview = input(f"{Colors.CYAN}İlk 30 kelimeyi görmek ister misiniz? (e/h): {Colors.END}").lower()
       
        if preview == 'e':
            print(f"\n{Colors.YELLOW}═══ ÖNİZLEME ═══{Colors.END}\n")
            for i, word in enumerate(sorted(self.wordlist)[:30], 1):
                print(f"{Colors.CYAN}{i:2d}.{Colors.END} {word}")
           
            if len(self.wordlist) > 30:
                print(f"\n{Colors.YELLOW}... ve {len(self.wordlist) - 30:,} kelime daha{Colors.END}\n")
   
    def run(self):
        """Ana program"""
        self.print_banner()
       
        try:
            self.setup()
            self.collect_data()
            self.generate_wordlist()
            self.save_wordlist()
            self.show_preview()
           
            print(f"{Colors.GREEN}{Colors.BOLD}Teşekkürler! ListGenerateX kullandığınız için teşekkürler.{Colors.END}\n")
           
        except KeyboardInterrupt:
            print(f"\n\n{Colors.RED}[!] İşlem kullanıcı tarafından iptal edildi.{Colors.END}\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Colors.RED}[!] Beklenmeyen hata: {e}{Colors.END}\n")
            sys.exit(1)


if __name__ == "__main__":
    generator = ListGenerateX()
    generator.run()
