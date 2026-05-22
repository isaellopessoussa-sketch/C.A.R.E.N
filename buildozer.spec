- name: Compilando o APK com Buildozer
      run: |
        # Aceita automaticamente todas as licenças do Android SDK antes do build
        mkdir -p ~/.buildozer/android/platform/android-sdk/licenses
        echo -e "\n89645534d78d0b54dcc1696dd4213cd44c34af3a\n2842d31bdaab1715cde24767544b66c50d6f6040\nd56f5187479451eabf01fb74bf36db4169f4b37d" > ~/.buildozer/android/platform/android-sdk/licenses/android-sdk-license
        
        # Roda o buildozer aceitando os termos restantes por comando
        yes | buildozer android debug
      env:
        BUILDOZER_ALLOW_KIVY_NEW_DESIGN: 1
