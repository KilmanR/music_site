#!/bin/bash

echo "🔧 Исправление ClamAV FreshClam..."
echo ""

# 1. Остановить сервис
echo "1. Остановка сервиса..."
sudo systemctl stop clamav-freshclam
sudo systemctl reset-failed clamav-freshclam

# 2. Создать бэкап конфига
echo "2. Создание бэкапа конфига..."
sudo cp /etc/clamav/freshclam.conf /etc/clamav/freshclam.conf.backup

# 3. Исправить конфиг
echo "3. Исправление конфига..."
sudo sed -i 's/^Checks.*/Checks 2/' /etc/clamav/freshclam.conf
sudo sed -i 's/^NotifyClamd/#NotifyClamd/' /etc/clamav/freshclam.conf

# Проверить, что Changes применились
if grep -q "^Checks 2" /etc/clamav/freshclam.conf; then
    echo "✅ Checks установлен в 2 (2 раза в день)"
else
    echo "⚠️ Checks не найден, добавляем..."
    echo "Checks 2" | sudo tee -a /etc/clamav/freshclam.conf
fi

if grep -q "^#NotifyClamd" /etc/clamav/freshclam.conf; then
    echo "✅ NotifyClamd закомментирован"
fi

# 4. Включить и запустить сервис
echo "4. Включение и запуск сервиса..."
sudo systemctl enable clamav-freshclam
sudo systemctl start clamav-freshclam

# 5. Показать статус
echo ""
echo "📊 Статус сервиса:"
sudo systemctl status clamav-freshclam --no-pager

echo ""
echo "✅ Готово!"
echo " Обновление заблокировано до: 2026-06-08 18:36:27"
echo "📅 Завтра после 18:40 сервис обновится автоматически"
echo ""
echo "Проверить завтра: sudo freshclam"
