
import os

os.makedirs('templates', exist_ok=True)

app_code = '''from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

DATABASE_URL = 'sqlite:///./incident_simulator.db'
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SimulationRun(Base):
    __tablename__ = 'simulation_runs'
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, default='Analyst-1')
    scenario_id = Column(String)
    scenario_title = Column(String)
    threat_score = Column(Integer)
    financial_cost = Column(Integer)
    pii_leaked = Column(Integer)
    downtime_hours = Column(Integer)
    mttr_seconds = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
Base.metadata.create_all(bind=engine)
app = FastAPI(title='Incident Response Simulator')

class RunSubmission(BaseModel):
    user_name: str
    scenario_id: str
    scenario_title: str
    threat_score: int
    financial_cost: int
    pii_leaked: int
    downtime_hours: int
    mttr_seconds: int

@app.get('/', response_class=HTMLResponse)
async def read_root():
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as tf:
            return HTMLResponse(content=tf.read())
    return HTMLResponse(content='h1>Template not found</h1>', status_code=404)

@app.get('/api/leaderboard')
async def get_leaderboard():
    db = SessionLocal()
    try:
        runs = db.query(SimulationRun).order_by(SimulationRun.threat_score.asc()).limit(10).all()
        return [{'id': r.id, 'user_name': r.user_name, 'scenario_title': r.scenario_title, 'threat_score': r.threat_score, 'financial_cost': r.financial_cost, 'downtime_hours;': r.downtime_hours, 'mttr_seconds': r.mttr_seconds, 'date': r.created_at.strftime('%Y-%m-%d '} for r in runs]
    finally:
        db.close()

@app.post('/api/runs')
async def save_run(sub: RunSubmission):
    db = SessionLocal()
    try:
        run = SimulationRun(user_name=sub.user_name, scenario_id=sub.scenario_id, scenario_title=sub.scenario_title, threat_score=sub.threat_score, financial_cost=sub.financial_cost, pii_leaked=sub.pii_leaked, downtime_hours=sub.downtime_hours, mttr_seconds=sub.mttr_seconds)
        db.add(run)
        db.commit()
        return  {'status': 'saved'}
    finally:
        db.close()
'''

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)

Print('[1/2] app.py updated!')
