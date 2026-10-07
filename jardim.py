from sqlalchemy import create_engine, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import List
import os
from dotenv import load_dotenv

class Base(DeclarativeBase):
    pass


class Jardim(Base):
    __tablename__ = "tabela_jardim"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(250))
    localizacao: Mapped[str] = mapped_column(Text)
    proprietario: Mapped[str] = mapped_column(Text)

    flores: Mapped[List["FloresNoJardim"]] = relationship(
        back_populates="jardim"
    )


class Flores(Base):
    __tablename__ = "tabela_flores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(250))
    tamanho: Mapped[str] = mapped_column(String(30))
    pais_origem: Mapped[str] = mapped_column(String(30))
    jardim: Mapped[List["FloresNoJardim"]] = relationship(
        back_populates="Flores"
    )


class FloresNoJardim(Base):
    __tablename__ = "tabela_flores_no_jardim"

    # chave estrangeira
    Flores_id: Mapped[int] = mapped_column(
        ForeignKey("tabela_flores.id"),
        primary_key=True
    )

    # chave estrangeira
    Jardim_id: Mapped[int] = mapped_column(
        ForeignKey("tabela_jardim.id"),
        primary_key=True
    )

    # atributos de acesso ao objeto
    Flores: Mapped["Flores"] = relationship(
        back_populates="jardim"
    )

    jardim: Mapped["Jardim"] = relationship(
        back_populates="flores"
    )

    nome_cientifico: Mapped[str] = mapped_column(String(250))
    cor: Mapped[str] = mapped_column(String(250))

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

engine = create_engine(
f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

Base.metadata.create_all(engine)


with Session(engine) as session:

    j1 = Jardim(
        nome="Jardim dos Sóis",
        localizacao="Jardim América",
        proprietario="Natalia"
    )

    f1 = Flores(nome="lírio", tamanho="médio", pais_origem="Japão")
    f2 = Flores(nome="tulipa", tamanho="médio", pais_origem="Turquia")
    f3 = Flores(nome="margarida", tamanho="pequeno", pais_origem="Reino Unido")
    f4 = Flores(nome="girassol", tamanho="grande", pais_origem="Estados Unidos")

    fj1 = FloresNoJardim(
        Flores=f1,
        jardim=j1,
        nome_cientifico="Lilium",
        cor="rosa"
    )

    fj2 = FloresNoJardim(
        Flores=f2,
        jardim=j1,
        nome_cientifico="Tulipa",
        cor="vermelha"
    )

    fj3 = FloresNoJardim(
        Flores=f3,
        jardim=j1,
        nome_cientifico="Bellis perennis",
        cor="branca"
    )

    fj4 = FloresNoJardim(
        Flores=f4,
        jardim=j1,
        nome_cientifico="Helianthus",
        cor="amarela"
    )

    # adiciona o jardim e todos os objetos relacionados
    session.add(j1)

    # salva tudo
    session.commit()

    print("A tabela foi criada (se não existia) e os dados do jardim foram inseridos.")
    print(f"O jardim chamado {j1.nome} foi salvo sob o número {j1.id}.")

    print("Flores no Jardim:")

    for item in j1.flores:
        print(item.Flores.nome, item.nome_cientifico, item.cor)

#recuperando meu commit 
#ass: Mari