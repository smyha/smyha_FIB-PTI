#!/bin/bash

# Script per compilar el document LaTeX de la pràctica
# Autor: Sergio Shmyhelskyy Yaskevych & Alex Lafuente Gonzalez
# Curs: PTI-FIB

echo "🔧 Compilant informe LaTeX..."

# Verificar que pdflatex està instal·lat
if ! command -v pdflatex &> /dev/null; then
    echo "❌ Error: pdflatex no està instal·lat."
    echo "   Instal·la una distribució LaTeX com TeX Live o MiKTeX."
    exit 1
fi

# Nom del fitxer LaTeX (sense extensió)
LATEX_FILE="informe_practica_servlets"

echo "📄 Compilant ${LATEX_FILE}.tex..."

# Primera compilació
echo "   Primera passada..."
pdflatex -interaction=nonstopmode "${LATEX_FILE}.tex" > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Error en la primera compilació. Executant amb output detallat:"
    pdflatex "${LATEX_FILE}.tex"
    exit 1
fi

# Segona compilació per resoldre referències
echo "   Segona passada (referències)..."
pdflatex -interaction=nonstopmode "${LATEX_FILE}.tex" > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Error en la segona compilació. Executant amb output detallat:"
    pdflatex "${LATEX_FILE}.tex"
    exit 1
fi

# Tercera compilació per assegurar-se que tot està correcte
echo "   Tercera passada (final)..."
pdflatex -interaction=nonstopmode "${LATEX_FILE}.tex" > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Error en la tercera compilació. Executant amb output detallat:"
    pdflatex "${LATEX_FILE}.tex"
    exit 1
fi

echo "✅ Compilació exitosa!"

# Netejar fitxers temporals
echo "🧹 Netejant fitxers temporals..."
rm -f *.aux *.log *.toc *.out *.fls *.fdb_latexmk *.synctex.gz

# Verificar que el PDF s'ha creat
if [ -f "${LATEX_FILE}.pdf" ]; then
    echo "📋 PDF generat: ${LATEX_FILE}.pdf"
    echo "📊 Mida del fitxer: $(du -h ${LATEX_FILE}.pdf | cut -f1)"
    
    # Intentar obrir el PDF automàticament (segons l'OS)
    if command -v xdg-open &> /dev/null; then
        echo "🔍 Obrint PDF amb xdg-open..."
        xdg-open "${LATEX_FILE}.pdf" &
    elif command -v open &> /dev/null; then
        echo "🔍 Obrint PDF amb open (macOS)..."
        open "${LATEX_FILE}.pdf" &
    elif command -v start &> /dev/null; then
        echo "🔍 Obrint PDF amb start (Windows)..."
        start "${LATEX_FILE}.pdf" &
    else
        echo "ℹ️  Obre manualment el fitxer: ${LATEX_FILE}.pdf"
    fi
else
    echo "❌ Error: No s'ha pogut generar el PDF"
    exit 1
fi

echo "🎉 Procés completat amb èxit!"
