from flask import Flask, render_template, request
import sympy as sp
from solver import identificar_funcao, resolver_e_explicar, plotar_grafico

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-segura'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        entrada = request.form.get('expression')
        try:
            # Substitui ^ por ** para potências
            funcao_str = entrada.replace('^', '**').strip()
            funcao = sp.sympify(funcao_str)
            x = sp.symbols('x')

            tipo = identificar_funcao(funcao)

            if tipo == "outro":
                return render_template('index.html', error="Função não suportada. Use apenas funções afins ou quadráticas.")

            # Extrair coeficientes
            if tipo == "constante":
                a, b, c = 0, 0, float(funcao)
            else:
                poly = funcao.as_poly(x)
                all_coeffs = poly.all_coeffs()
                if tipo == "afim":
                    a, b = all_coeffs if len(all_coeffs) == 2 else (all_coeffs[0], 0)
                    c = 0
                else: # quadrática
                    a, b, c = all_coeffs if len(all_coeffs) == 3 else (all_coeffs[0], all_coeffs[1], 0) if len(all_coeffs) == 2 else (all_coeffs[0], 0, 0)

            # Resolução e Gráfico
            passos, raizes, pontos_notaveis = resolver_e_explicar(tipo, a, b, c)
            grafico_b64 = plotar_grafico(funcao, raizes, tipo, a, b, c, pontos_notaveis)
            
            return render_template('results.html', 
                                   funcao_original=entrada,
                                   passos=passos, 
                                   grafico=grafico_b64)

        except Exception as e:
            return render_template('index.html', error=f"Erro ao processar a função: {e}. Verifique a sintaxe (ex: 2*x**2 + 3*x - 5).")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
