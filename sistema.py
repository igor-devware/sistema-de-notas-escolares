from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Avaliacao:
    nota: float
    peso: float
    
    def __post_init__(self):
        if not (0 <= self.nota <= 10):
            raise ValueError(f"Nota inválida: {self.nota}. Deve estar entre 0 e 10.")
        if self.peso <= 0:
            raise ValueError(f"Peso inválido: {self.peso}. Deve ser positivo.")

@dataclass
class Disciplina:
    nome: str
    avaliacoes: List[Avaliacao]
    
    def __post_init__(self):
        if not self.avaliacoes:
            raise ValueError(f"Disciplina '{self.nome}' sem avaliações.")

    def calcular_media(self) -> float:
        soma_notas = sum(av.nota * av.peso for av in self.avaliacoes)
        soma_pesos = sum(av.peso for av in self.avaliacoes)
        return round(soma_notas / soma_pesos, 2)

@dataclass
class Aluno:
    nome: str
    matricula: str
    disciplinas: List[Disciplina]

def aplicar_recuperacao(avaliacoes: List[Avaliacao], nota_recuperacao: float) -> List[Avaliacao]:
    if not avaliacoes:
        return avaliacoes

    novas_avaliacoes = [Avaliacao(av.nota, av.peso) for av in avaliacoes]
    menor_idx = min(range(len(novas_avaliacoes)), key=lambda i: novas_avaliacoes[i].nota)
    
    if nota_recuperacao > novas_avaliacoes[menor_idx].nota:
        novas_avaliacoes[menor_idx].nota = nota_recuperacao
    
    return novas_avaliacoes

def verificar_aprovacao(media: float, media_minima: float = 6.0) -> bool:
    return media >= media_minima

class SistemaNotas:
    def __init__(self, media_minima: float = 6.0):
        self.media_minima = media_minima
    
    def processar_aluno(self, aluno: Aluno) -> Dict[str, Any]:
        resultado_disciplinas = []
        
        for disciplina in aluno.disciplinas:
            media = disciplina.calcular_media()
            aprovado = verificar_aprovacao(media, self.media_minima)
            
            resultado_disciplinas.append({
                'nome': disciplina.nome,
                'media': media,
                'aprovado': aprovado
            })
        
        medias = [d['media'] for d in resultado_disciplinas]
        media_geral = round(sum(medias) / len(medias), 2) if medias else 0.0
        aprovado_geral = all(d['aprovado'] for d in resultado_disciplinas)
        
        return {
            'nome': aluno.nome,
            'matricula': aluno.matricula,
            'disciplinas': resultado_disciplinas,
            'media_geral': media_geral,
            'aprovado_geral': aprovado_geral
        }
    
    def gerar_relatorio(self, alunos: List[Aluno]) -> str:
        line = "=" * 80
        relatorio = [line, "RELATÓRIO DE DESEMPENHO ESCOLAR".center(80), line, ""]
        
        for aluno in alunos:
            res = self.processar_aluno(aluno)
            relatorio.append(f"ALUNO: {res['nome']} (Matrícula: {res['matricula']})")
            relatorio.append("-" * 80)
            
            for disc in res['disciplinas']:
                status = "APROVADO" if disc['aprovado'] else "REPROVADO"
                relatorio.append(f"  {disc['nome']:<30} Média: {disc['media']:>5.2f}  {status}")
            
            relatorio.append("-" * 80)
            relatorio.append(f"  MÉDIA GERAL: {res['media_geral']:.2f}")
            status_geral = "APROVADO" if res['aprovado_geral'] else "REPROVADO"
            relatorio.append(f"  STATUS FINAL: {status_geral}\n")
        
        relatorio.append(line)
        return "\n".join(relatorio)

if __name__ == "__main__":
    aluno1 = Aluno(
        nome="João Silva",
        matricula="2024001",
        disciplinas=[
            Disciplina("Matemática", [Avaliacao(8.5, 2), Avaliacao(7.0, 2), Avaliacao(9.0, 3)]),
            Disciplina("Português", [Avaliacao(6.5, 1), Avaliacao(7.5, 1), Avaliacao(8.0, 2)]),
        ]
    )
    
    aluno2 = Aluno(
        nome="Maria Santos",
        matricula="2024002",
        disciplinas=[
            Disciplina("Matemática", [Avaliacao(5.0, 2), Avaliacao(4.5, 2), Avaliacao(6.0, 3)]),
            Disciplina("Português", [Avaliacao(9.0, 1), Avaliacao(8.5, 1), Avaliacao(9.5, 2)]),
        ]
    )

    sistema = SistemaNotas(media_minima=6.0)
    print(sistema.gerar_relatorio([aluno1, aluno2]))
    
    print(" TESTE: Aplicando recuperação para Maria em Matemática ".center(80, "="))
    disc_mat = aluno2.disciplinas[0]
    print(f"Média original: {disc_mat.calcular_media()}")
    
    avaliacoes_com_rec = aplicar_recuperacao(disc_mat.avaliacoes, nota_recuperacao=7.0)
    temp_disc = Disciplina("Matemática Rec", avaliacoes_com_rec)
    print(f"Média após recuperação (7.0 no lugar da menor nota): {temp_disc.calcular_media()}")
