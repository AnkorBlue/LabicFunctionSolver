import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

# Configura o Matplotlib para não usar a interface gráfica
plt.switch_backend('Agg')

x = sp.symbols('x')

def formatar_numero(valor):
    """Formata um número para exibição, convertendo para inteiro se possível."""
    if isinstance(valor, str) and valor == "Todos":
        return "Todos os números reais"
    try:
        f_valor = float(valor)
        return f"{int(f_valor)}" if f_valor.is_integer() else f"{f_valor:.2f}".replace('.', ',')
    except (ValueError, TypeError):
        return str(valor)

def identificar_funcao(expr):
    """Identifica se a função é afim ou quadrática."""
    if not expr.has(x):
        return "constante"
        
    try:
        grau = expr.as_poly(x).degree()
        if grau == 1:
            return "afim"
        elif grau == 2:
            return "quadrática"
        else:
            return "outro"
    except (sp.PolynomialError, AttributeError):
        return "outro"


def analisar_variacao(a, tipo, vertice_x=None):
    """Gera a análise de crescimento/decrescimento da função."""
    variacao_str = "<strong>Análise de crescimento/decrescimento:</strong><br>"
    if tipo == "afim":
        if a > 0:
            variacao_str += "A função é <strong>crescente</strong>, pois o coeficiente 'a' é positivo (a > 0)."
        elif a < 0:
            variacao_str += "A função é <strong>decrescente</strong>, pois o coeficiente 'a' é negativo (a < 0)."
        else:
            variacao_str += "A função é <strong>constante</strong>, pois o coeficiente 'a' é zero (a = 0)."
    elif tipo == "quadrática":
        concavidade = "para cima (a > 0)" if a > 0 else "para baixo (a < 0)"
        variacao_str += f"A parábola tem concavidade voltada <strong>{concavidade}</strong>.<br>"
        vx_formatado = formatar_numero(vertice_x)
        if a > 0:
            variacao_str += f"A função é <strong>decrescente</strong> para x < {vx_formatado} e <strong>crescente</strong> para x > {vx_formatado}."
        else:
            variacao_str += f"A função é <strong>crescente</strong> para x < {vx_formatado} e <strong>decrescente</strong> para x > {vx_formatado}."
    return variacao_str
    
def resolver_e_explicar(tipo, a, b, c):
    """Resolve a função passo a passo e retorna a explicação em LaTeX e as raízes."""
    passos = []
    raizes = []
    pontos_notaveis = []

    # Leitura dos coeficientes
    passos.append("<h3>1. Leitura dos Coeficientes</h3>")
    if tipo == "afim":
        passos.append(f"A função é do tipo <strong>f(x) = ax + b</strong>.<br>Os coeficientes são: a = {formatar_numero(a)}, b = {formatar_numero(b)}.")
    elif tipo == "quadrática":
        passos.append(f"A função é do tipo <strong>f(x) = ax² + bx + c</strong>.<br>Os coeficientes são: a = {formatar_numero(a)}, b = {formatar_numero(b)}, c = {formatar_numero(c)}.")
    else: # Constante
        passos.append(f"A função é do tipo <strong>f(x) = c</strong>.<br>O coeficiente é: c = {formatar_numero(c)}.")

    # Resolução
    if tipo == "afim":
        passos.append("<h3>2. Encontrando a Raiz</h3>")
        passos.append("Para encontrar a raiz, fazemos f(x) = 0:<br>")
        passos.append(f"$$ {a}x + {b} = 0 $$")
        passos.append(f"$$ {a}x = {-b} $$")
        
        if a != 0:
            raiz = -b / a
            raizes = [raiz]
            passos.append(f"$$ x = \\frac{{{-b}}}{{{a}}} = {formatar_numero(raiz)} $$")
            pontos_notaveis.append((raiz, 0))
        else: # a == 0, função constante
             passos.append("Como 'a' é zero, a função é constante e não possui uma raiz única (não cruza o eixo x, a menos que b=0).")
        
        passos.append("<h3>3. Intercepto Y</h3>")
        passos.append(f"O ponto onde a reta cruza o eixo Y é o valor de 'b'.<br>f(0) = {formatar_numero(b)}")
        pontos_notaveis.append((0, b))

    elif tipo == "quadrática":
        # Cálculo de Delta
        passos.append("<h3>2. Calculando o Discriminante (Delta)</h3>")
        passos.append("A fórmula de delta é: $$ \\Delta = b^2 - 4ac $$")
        delta = b**2 - 4*a*c
        passos.append(f"$$ \\Delta = ({b})^2 - 4 \\cdot ({a}) \\cdot ({c}) = {formatar_numero(delta)} $$")

        # Fórmula de Bhaskara
        passos.append("<h3>3. Aplicando a Fórmula de Bhaskara</h3>")
        passos.append("A fórmula de Bhaskara é: $$ x = \\frac{{-b \\pm \\sqrt{{\\Delta}}}}{{2a}} $$")

        if delta < 0:
            passos.append("Como o valor de Delta é negativo, a função não possui raízes reais.")
        else:
            raiz1 = (-b + sp.sqrt(delta)) / (2 * a)
            raiz2 = (-b - sp.sqrt(delta)) / (2 * a)
            raizes = [raiz1]
            passos.append(f"$$ x_1 = \\frac{{-({b}) + \\sqrt{{{delta}}}}}{{2 \\cdot ({a})}} = {formatar_numero(raiz1)} $$")

            if delta > 0:
                raizes.append(raiz2)
                passos.append(f"$$ x_2 = \\frac{{-({b}) - \\sqrt{{{delta}}}}}{{2 \\cdot ({a})}} = {formatar_numero(raiz2)} $$")
            else:
                 passos.append("Como Delta é zero, as duas raízes são iguais (x₁ = x₂).")
        
        # Vértice da Parábola
        vertice_x = -b / (2 * a)
        vertice_y = a * vertice_x**2 + b * vertice_x + c
        pontos_notaveis.append((vertice_x, vertice_y))
        passos.append("<h3>4. Vértice da Parábola</h3>")
        passos.append("As coordenadas do vértice (V) são dadas por:")
        passos.append(f"$$ x_v = \\frac{{-b}}{{2a}} = \\frac{{-({b})}}{{2 \\cdot ({a})}} = {formatar_numero(vertice_x)} $$")
        passos.append(f"$$ y_v = f(x_v) = {formatar_numero(vertice_y)} $$")
        passos.append(f"Portanto, o vértice é V({formatar_numero(vertice_x)}, {formatar_numero(vertice_y)}).")
        
        # Intercepto Y
        passos.append("<h3>5. Intercepto Y</h3>")
        passos.append(f"O ponto onde a parábola cruza o eixo Y é o valor de 'c'.<br>f(0) = {formatar_numero(c)}")
        pontos_notaveis.append((0, c))
    
    # Análise de Variação
    vertice_x_val = -b / (2*a) if tipo == "quadrática" else None
    variacao = analisar_variacao(a, tipo, vertice_x_val)
    passos.append(f"<h3>{ '6.' if tipo == 'quadrática' else '4.'} Variação da Função</h3>")
    passos.append(variacao)

    return "<br>".join(passos), raizes, pontos_notaveis


def plotar_grafico(funcao, raizes, tipo, a, b, c, pontos_notaveis):
    """Gera o gráfico da função e retorna como uma imagem em base64."""
    plt.figure(figsize=(8, 6))
    f_lambdified = sp.lambdify(x, funcao, modules=['numpy'])

    x_numericas = [p[0] for p in pontos_notaveis if isinstance(p[0], (int, float, sp.Number))]
    x_numericas += [r for r in raizes if isinstance(r, (int, float, sp.Number))]

    if not x_numericas:
        x_range = np.linspace(-10, 10, 400)
    else:
        min_x, max_x = min(x_numericas), max(x_numericas)
        padding = max(2, (max_x - min_x) * 0.2)
        x_range = np.linspace(min_x - padding, max_x + padding, 400)

    y_range = f_lambdified(x_range)

    plt.plot(x_range, y_range, label=f'f(x) = {sp.latex(funcao)}', color='#007BFF')
    
    # Eixos
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True, linestyle='--', alpha=0.6)

    # Raízes
    if raizes:
        raizes_num = [float(r) for r in raizes]
        plt.scatter(raizes_num, [0]*len(raizes_num), color='red', zorder=5, label='Raízes')
        for r in raizes_num:
            plt.annotate(f'({formatar_numero(r)}, 0)', (r, 0), textcoords="offset points", xytext=(0,10), ha='center')

    # Pontos Notáveis
    if tipo == "quadrática":
        vx, yv = pontos_notaveis[0]
        plt.scatter([vx], [yv], color='green', zorder=5, label='Vértice')
        plt.annotate(f'V({formatar_numero(vx)}, {formatar_numero(yv)})', (vx, yv), textcoords="offset points", xytext=(0,-15), ha='center')

    # Intercepto Y
    intercepto_y = c if tipo == "quadrática" else b
    plt.scatter([0], [intercepto_y], color='#6f42c1', zorder=5, label='Intercepto Y')
    plt.annotate(f'(0, {formatar_numero(intercepto_y)})', (0, intercepto_y), textcoords="offset points", xytext=(0,10), ha='center')

    plt.title(f"Gráfico da Função {tipo.capitalize()}", fontsize=16)
    plt.xlabel("x", fontsize=12)
    plt.ylabel("f(x)", fontsize=12)
    plt.legend()
    plt.tight_layout()

    # Salva o gráfico em um buffer de memória
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_base64}"