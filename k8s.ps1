param (
    [switch] $dev,
    [switch] $build,
    [switch] $delete
 )

$K8S_CONF_FOLDER="kubernetes"
$SERVICE = "nginx-prod-server-svc"
$API_APP = "fastapi-app"
$PROD_APP = "nginx-app"
$DEV_APP = "react-app"
$SECRET_CFG = "currency-app-config"
$ENV_FILE = "./.env"

 $symbols = [PSCustomObject] @{

    FAIL = [char]::ConvertFromUtf32(0x1F6AB)
    SUCCESS = [char]::ConvertFromUtf32(0x2705)
    PROCESSING = [char]::ConvertFromUtf32(0x25B6)
}

 function Write-ClrOP($ForegroundColor)
{
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor

    if ($args) {
        Write-Output $args
    }
    else {
        $input | Write-Output
    }

    $host.UI.RawUI.ForegroundColor = $fc
}

function Get-Pod-Status($APP){
    return kubectl get pods -l app=$APP -o jsonpath='{.items[*].status.containerStatuses[0].ready}'
}

function Wait-Pod-Status($APP, $status="true"){

    if($status -eq "false"){
        $status = $null
    }

    while((Get-Pod-Status $APP) -ne $status){
        Start-Sleep -Seconds 5
    }
}

if ($null -eq $env:MINIKUBE_ACTIVE_DOCKERD){
    Write-ClrOP green "$($symbols.PROCESSING) Setting environment to use minikube...`n"
    minikube -p minikube docker-env --shell powershell | Invoke-Expression
}

if($delete -and ($build -or $dev)){
    Write-ClrOP red "`n$($symbols.FAIL) Incompatible options: Cannot use -delete with any other option`n"
    Exit
 }

if($dev){
    $SERVICE = "react-dev-server-svc"
}

$build_docker_images = {
    Write-ClrOP green "$($symbols.PROCESSING) Building Docker images...`n"
    docker compose build
}

$delete_deployments = {

    Write-ClrOP red "$($symbols.PROCESSING) Deleting deployments..."

    Invoke-Expression "kubectl delete -f ./$K8S_CONF_FOLDER" -ErrorVariable ErrOutput 2>&1 >$null

    if($ErrOutput -ne ""){
        Write-ClrOP red "$($symbols.FAIL) No deployments to delete!`n"
    }
    else{
        Write-ClrOP red "$($symbols.PROCESSING) Waiting for pods to terminate..."
        Wait-Pod-Status $PROD_APP "false"
        Wait-Pod-Status $DEV_APP "false"
        Write-ClrOP green "$($symbols.SUCCESS) Pods terminated!`n"
    }
}

$setup_secrets = {

    Write-ClrOP green "$($symbols.PROCESSING) Setting up configuration..."
    Invoke-Expression "kubectl create secret generic $SECRET_CFG --from-env-file=$ENV_FILE" -ErrorVariable ErrOutput 2>&1 >$null

    if($ErrOutput -ne ""){
        Write-ClrOP green "$($symbols.SUCCESS) Configuration already exists`n"
    }
}

$delete_secrets = {

    Write-ClrOP red "$($symbols.PROCESSING) Deleting configuration..."
    Invoke-Expression "kubectl delete secret $SECRET_CFG" -ErrorVariable ErrOutput 2>&1 >$null

    if($ErrOutput -ne ""){
        Write-ClrOP red "$($symbols.FAIL) No confguration to delete!`n"
    }
    else{
        Write-ClrOP green "$($symbols.SUCCESS) Configuration deleted!`n"
    }
}

if($delete){
    Invoke-Command -ScriptBlock $delete_deployments
    Invoke-Command -ScriptBlock $delete_secrets
    Exit
}

if($build){
    Invoke-Command -ScriptBlock $build_docker_images
}

# Write-ClrOP green "$($symbols.PROCESSING) Setting up configuration..."
# kubectl create secret generic $SECRET_CFG --from-env-file=$ENV_FILE | Out-Null

Invoke-Command -ScriptBlock $setup_secrets

Write-ClrOP green "$($symbols.PROCESSING) Starting up Kubernetes cluster in minikube...`n"
kubectl apply -f ./$K8S_CONF_FOLDER | Out-Null

Write-ClrOP yellow "$($symbols.PROCESSING) Setting up services..."
Wait-Pod-Status $API_APP
Write-ClrOP yellow "$($symbols.SUCCESS) Setup complete!`n"

Write-ClrOP green "$($symbols.PROCESSING) Exposing $SERVICE service for deployment..."

$port = kubectl get svc $SERVICE -o jsonpath='{.spec.ports[].port}'
Write-ClrOP yellow "$($symbols.SUCCESS) Access the $SERVICE on http://localhost:$port`n"

& kubectl port-forward service/$SERVICE ${port}:$port --address 0.0.0.0
